#!/usr/bin/env python3
"""
VRT Auto-Scheduler — assigns dates + statuses to all tracker items for the April 17 launch.

Usage:
  python3 auto-scheduler.py              # Full run: audit + schedule + write to Notion
  python3 auto-scheduler.py --audit      # Audit only, print report, no date changes
  python3 auto-scheduler.py --dry-run    # Show assignments without writing to Notion
  python3 auto-scheduler.py --recalculate  # Re-run on remaining non-Done tasks only
"""

import json, subprocess, os, sys, time
from datetime import datetime, date, timedelta

# ── Config ──────────────────────────────────────────────────────────────────

_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(_env_path) and not os.environ.get("NOTION_API_KEY"):
    with open(_env_path) as _f:
        for _line in _f:
            if "=" in _line and not _line.startswith("#"):
                k, v = _line.strip().split("=", 1)
                os.environ[k] = v

API_KEY = os.environ.get("NOTION_API_KEY", "")
TRACKER_DB = "30a5308b-6bc5-8171-a2c3-d89200293d13"
LAUNCH_DATE = date(2026, 4, 17)

# Phase definitions (inclusive)
PHASES = [
    {"name": "Foundation",    "start": date(2026, 2, 18), "end": date(2026, 3, 8)},
    {"name": "Build Sprint",  "start": date(2026, 3, 9),  "end": date(2026, 3, 29)},
    {"name": "Polish & Test", "start": date(2026, 3, 30), "end": date(2026, 4, 10)},
    {"name": "Launch Prep",   "start": date(2026, 4, 11), "end": date(2026, 4, 16)},
]

# Owner daily task capacity (7-day work weeks)
OWNER_CAPACITY = {"Alon": 3, "Matan": 2, "Sahar": 3}
DEFAULT_OWNER_BY_DEPT = {"Marketing": "Sahar", "Product": "Alon", "R&D": "Matan"}

API_DELAY = 0.35  # seconds between Notion writes

# Phase-affinity keywords: map task name patterns → phase index
PHASE_KEYWORDS = {
    0: ["prd", "brand", "design system", "infra", "setup", "plan", "strategy", "research",
        "brief", "identity", "guidelines", "marketing plan", "content plan"],
    1: ["develop", "build", "landing page", "content production", "youtube", "component",
        "implement", "create", "code", "record", "shoot", "write content"],
    2: ["qa", "test", "payment", "polish", "fix", "review", "stripe", "subscription",
        "beta", "iterate", "optimize"],
    3: ["launch", "announce", "final", "checklist", "go live", "deploy prod"],
}


# ── Notion API ──────────────────────────────────────────────────────────────

def notion_request(method, endpoint, payload=None):
    cmd = ["curl", "-s", "-X", method,
           f"https://api.notion.com/v1/{endpoint}",
           "-H", f"Authorization: Bearer {API_KEY}",
           "-H", "Notion-Version: 2022-06-28",
           "-H", "Content-Type: application/json"]
    if payload:
        cmd += ["-d", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def query_all_items():
    """Fetch all items from VRT Tracker (handles pagination)."""
    items = []
    payload = {"page_size": 100}
    while True:
        data = notion_request("POST", f"databases/{TRACKER_DB}/query", payload)
        for page in data.get("results", []):
            p = page["properties"]
            items.append({
                "id": page["id"],
                "name": "".join(t.get("plain_text", "") for t in p.get("Name", {}).get("title", [])),
                "department": (p.get("Department", {}).get("select") or {}).get("name", ""),
                "level": (p.get("Level", {}).get("select") or {}).get("name", ""),
                "status": (p.get("Status", {}).get("select") or {}).get("name", ""),
                "progress": p.get("Progress", {}).get("number", 0) or 0,
                "due": ((p.get("Due", {}).get("date") or {}).get("start", "") or "")[:10],
                "owner": (p.get("Owner", {}).get("select") or {}).get("name", ""),
                "parent_ids": [r["id"] for r in p.get("Parent", {}).get("relation", [])],
                "categories": [o["name"] for o in p.get("Category", {}).get("multi_select", [])],
            })
        if data.get("has_more"):
            payload["start_cursor"] = data["next_cursor"]
        else:
            break
    return items


def update_page(page_id, properties):
    """Write properties to a Notion page."""
    notion_request("PATCH", f"pages/{page_id}", {"properties": properties})


# ── Audit ───────────────────────────────────────────────────────────────────

def run_audit(items, write=False):
    """Validate and fix data coherency. Returns (fixes, warnings)."""
    id_map = {i["id"]: i for i in items}
    fixes = []
    warnings = []

    for item in items:
        props_to_write = {}

        # Status must be set
        if not item["status"]:
            item["status"] = "Not Started"
            props_to_write["Status"] = {"select": {"name": "Not Started"}}
            fixes.append(f"  Set Status → Not Started: {item['name']}")

        # Level must be set
        if item["level"] not in ("Goal", "Project", "Task"):
            warnings.append(f"  Missing/invalid Level: {item['name']} (level={item['level']!r})")

        # Department must match parent
        if item["parent_ids"]:
            parent = id_map.get(item["parent_ids"][0])
            if parent and parent["department"] and item["department"] != parent["department"]:
                old = item["department"]
                item["department"] = parent["department"]
                props_to_write["Department"] = {"select": {"name": parent["department"]}}
                fixes.append(f"  Fixed Department {old!r} → {parent['department']!r}: {item['name']}")

        # Owner must be set — infer from department
        if not item["owner"] and item["department"]:
            owner = DEFAULT_OWNER_BY_DEPT.get(item["department"], "Alon")
            item["owner"] = owner
            props_to_write["Owner"] = {"select": {"name": owner}}
            fixes.append(f"  Set Owner → {owner}: {item['name']}")

        # Orphan check
        if item["level"] == "Task" and not item["parent_ids"]:
            warnings.append(f"  Orphan Task (no parent Project): {item['name']}")
        if item["level"] == "Project" and not item["parent_ids"]:
            warnings.append(f"  Orphan Project (no parent Goal): {item['name']}")

        # Progress: Goals/Projects with all-Not-Started children should be 0
        if item["level"] in ("Goal", "Project"):
            children = [i for i in items if item["id"] in i["parent_ids"]]
            if children and all(c["status"] == "Not Started" for c in children) and item["progress"] != 0:
                item["progress"] = 0
                props_to_write["Progress"] = {"number": 0}
                fixes.append(f"  Reset Progress → 0: {item['name']}")

        if props_to_write and write:
            update_page(item["id"], props_to_write)
            time.sleep(API_DELAY)

    return fixes, warnings


# ── Scheduling ──────────────────────────────────────────────────────────────

def infer_priority(task):
    """Return priority 0-3 (lower = higher priority)."""
    name_lower = task["name"].lower()
    cats = [c.lower() for c in task.get("categories", [])]

    # Infrastructure/blocking tasks → P0
    if "infrastructure" in cats or "infra" in name_lower:
        return 0
    # Product department → P0
    if task["department"] == "Product":
        return 0
    # R&D → P1
    if task["department"] == "R&D":
        return 1
    # Marketing → P1-P2 (content is P1, rest P2)
    if task["department"] == "Marketing":
        if any(c in cats for c in ["content", "youtube"]):
            return 1
        return 2
    return 2


def infer_phase(task):
    """Return best-fit phase index (0-3) based on task name keywords."""
    name_lower = task["name"].lower()
    for phase_idx, keywords in PHASE_KEYWORDS.items():
        if any(kw in name_lower for kw in keywords):
            return phase_idx
    # Default: infer from department
    if task["department"] == "R&D":
        return 1  # Build Sprint
    if task["department"] == "Marketing":
        return 1  # Build Sprint (content production)
    return 0  # Foundation


DEPT_RANK = {"Product": 0, "R&D": 1, "Marketing": 2}


def schedule_tasks(items, recalculate=False):
    """Assign due dates to tasks based on priority, phase, and owner capacity."""
    id_map = {i["id"]: i for i in items}
    today = date.today()

    # Filter schedulable tasks
    tasks = [i for i in items if i["level"] == "Task" and i["status"] != "Done"]
    if recalculate:
        # Only reschedule tasks that are Not Started or whose due date is in the future
        tasks = [t for t in tasks if t["status"] != "Done"]

    # Enrich with priority + phase
    for t in tasks:
        t["_priority"] = infer_priority(t)
        t["_phase"] = infer_phase(t)

    # Sort: priority → phase → department rank → name
    tasks.sort(key=lambda t: (t["_priority"], t["_phase"],
                               DEPT_RANK.get(t["department"], 9), t["name"]))

    # Build owner calendars
    start_date = today if recalculate else PHASES[0]["start"]
    calendars = {}  # owner → {date_str: count}
    for owner in OWNER_CAPACITY:
        calendars[owner] = {}

    assignments = []
    overflow = []

    for t in tasks:
        owner = t["owner"] or "Alon"
        cap = OWNER_CAPACITY.get(owner, 2)
        phase = PHASES[t["_phase"]]

        # Phase window — for recalculate, don't schedule in the past
        phase_start = max(phase["start"], start_date)
        phase_end = phase["end"]

        assigned = False
        d = phase_start
        while d <= phase_end:
            day_key = d.isoformat()
            used = calendars.get(owner, {}).get(day_key, 0)
            if used < cap:
                calendars.setdefault(owner, {})[day_key] = used + 1
                t["_assigned_date"] = d.isoformat()
                assignments.append(t)
                assigned = True
                break
            d += timedelta(days=1)

        if not assigned:
            # Overflow: try next phases
            for pi in range(t["_phase"] + 1, len(PHASES)):
                next_phase = PHASES[pi]
                np_start = max(next_phase["start"], start_date)
                d = np_start
                while d <= next_phase["end"]:
                    day_key = d.isoformat()
                    used = calendars.get(owner, {}).get(day_key, 0)
                    if used < cap:
                        calendars.setdefault(owner, {})[day_key] = used + 1
                        t["_assigned_date"] = d.isoformat()
                        t["_phase"] = pi  # moved phase
                        assignments.append(t)
                        assigned = True
                        break
                    d += timedelta(days=1)
                if assigned:
                    break

            if not assigned:
                overflow.append(t)
                # Last resort: assign to launch date
                t["_assigned_date"] = LAUNCH_DATE.isoformat()
                assignments.append(t)

    # Derive Project/Goal dates from children
    projects = [i for i in items if i["level"] == "Project"]
    goals = [i for i in items if i["level"] == "Goal"]

    for proj in projects:
        child_dates = []
        for t in assignments:
            if proj["id"] in t["parent_ids"] and t.get("_assigned_date"):
                child_dates.append(t["_assigned_date"])
        if child_dates:
            proj["_start_date"] = min(child_dates)
            proj["_end_date"] = max(child_dates)

    for goal in goals:
        child_dates = []
        for proj in projects:
            if goal["id"] in proj["parent_ids"]:
                if proj.get("_start_date"):
                    child_dates.append(proj["_start_date"])
                if proj.get("_end_date"):
                    child_dates.append(proj["_end_date"])
        if child_dates:
            goal["_start_date"] = min(child_dates)
            goal["_end_date"] = max(child_dates)

    return assignments, projects, goals, overflow


def write_schedule(assignments, projects, goals):
    """Write Due dates + Status to Notion."""
    count = 0

    for t in assignments:
        props = {}
        if t.get("_assigned_date"):
            props["Due"] = {"date": {"start": t["_assigned_date"]}}
        if t["status"] == "" or not t["status"]:
            props["Status"] = {"select": {"name": "Not Started"}}
        if props:
            update_page(t["id"], props)
            count += 1
            time.sleep(API_DELAY)

    for proj in projects:
        if proj.get("_start_date") and proj.get("_end_date"):
            props = {"Due": {"date": {"start": proj["_start_date"], "end": proj["_end_date"]}}}
            update_page(proj["id"], props)
            count += 1
            time.sleep(API_DELAY)

    for goal in goals:
        if goal.get("_start_date") and goal.get("_end_date"):
            props = {"Due": {"date": {"start": goal["_start_date"], "end": goal["_end_date"]}}}
            update_page(goal["id"], props)
            count += 1
            time.sleep(API_DELAY)

    return count


# ── Reports ─────────────────────────────────────────────────────────────────

def print_audit_report(fixes, warnings):
    print(f"\n{'='*60}")
    print("DATA COHERENCY AUDIT")
    print(f"{'='*60}")
    if fixes:
        print(f"\nFixed ({len(fixes)}):")
        for f in fixes:
            print(f)
    else:
        print("\nNo fixes needed.")
    if warnings:
        print(f"\nWarnings ({len(warnings)}) — needs Alon's input:")
        for w in warnings:
            print(w)
    else:
        print("\nNo warnings.")
    print()


def print_schedule_report(assignments, overflow, items):
    phase_counts = {p["name"]: 0 for p in PHASES}
    owner_counts = {}
    for t in assignments:
        phase_name = PHASES[t["_phase"]]["name"]
        phase_counts[phase_name] = phase_counts.get(phase_name, 0) + 1
        owner_counts[t["owner"]] = owner_counts.get(t["owner"], 0) + 1

    print(f"\n{'='*60}")
    print("SCHEDULE SUMMARY")
    print(f"{'='*60}")
    print(f"\nTotal tasks scheduled: {len(assignments)}")
    print(f"\nPhase distribution:")
    for p in PHASES:
        cnt = phase_counts.get(p["name"], 0)
        print(f"  {p['name']} ({p['start']} → {p['end']}): {cnt} tasks")
    print(f"\nOwner distribution:")
    for owner, cnt in sorted(owner_counts.items()):
        print(f"  {owner}: {cnt} tasks")
    if overflow:
        print(f"\nOverflow warnings ({len(overflow)}) — couldn't fit in ideal phase:")
        for t in overflow:
            print(f"  {t['name']} ({t['owner']}, {t['department']})")
    print()


def print_dry_run(assignments):
    print(f"\n{'='*60}")
    print("DRY RUN — Proposed Assignments")
    print(f"{'='*60}\n")
    current_phase = None
    for t in sorted(assignments, key=lambda x: (x["_phase"], x.get("_assigned_date", ""))):
        phase_name = PHASES[t["_phase"]]["name"]
        if phase_name != current_phase:
            current_phase = phase_name
            print(f"\n── {phase_name} ──")
        print(f"  {t.get('_assigned_date', '???'):10s}  [{t['owner']:6s}]  {t['name']}")
    print()


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    args = set(sys.argv[1:])
    audit_only = "--audit" in args
    dry_run = "--dry-run" in args
    recalculate = "--recalculate" in args

    print("Fetching all VRT Tracker items...")
    items = query_all_items()
    print(f"  {len(items)} items found.")

    # Step 1: Audit
    should_write_audit = not audit_only or not dry_run  # always write fixes unless just previewing
    fixes, warnings = run_audit(items, write=(not dry_run and not audit_only))
    print_audit_report(fixes, warnings)

    if audit_only:
        print("Audit complete. Use --dry-run or no flags to also run scheduling.")
        return

    # Step 2: Schedule
    print("Running scheduler...")
    assignments, projects, goals, overflow = schedule_tasks(items, recalculate=recalculate)
    print_schedule_report(assignments, overflow, items)

    if dry_run:
        print_dry_run(assignments)
        print("Dry run complete. Remove --dry-run to write to Notion.")
        return

    # Step 3: Write to Notion
    print("Writing schedule to Notion...")
    count = write_schedule(assignments, projects, goals)
    print(f"  {count} pages updated.")

    # Also write audit fixes if not already done
    if fixes and not should_write_audit:
        print("Writing audit fixes to Notion...")
        run_audit(items, write=True)

    print(f"\nDone! {len(assignments)} tasks scheduled across {len(PHASES)} phases.")
    if overflow:
        print(f"  {len(overflow)} tasks overflowed their ideal phase (assigned to later phases).")


if __name__ == "__main__":
    main()
