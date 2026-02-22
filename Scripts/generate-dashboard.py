#!/usr/bin/env python3
"""
VRT Dashboard Generator
Pulls live data from the Notion VRT Tracker and generates a responsive HTML dashboard.
Run: python3 ~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py
"""

import json, subprocess, os
from datetime import datetime, date, timedelta

# Load .env from workspace root if NOTION_API_KEY not already set
_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(_env_path) and not os.environ.get("NOTION_API_KEY"):
    with open(_env_path) as _f:
        for _line in _f:
            if "=" in _line and not _line.startswith("#"):
                k, v = _line.strip().split("=", 1)
                os.environ[k] = v

API_KEY = os.environ.get("NOTION_API_KEY", "")
TRACKER_DB = "30a5308b-6bc5-8171-a2c3-d89200293d13"
TOOL_INV_DB = "3408692e-ca14-4886-8143-86ceb7f979e6"
LAUNCH_DATE = date(2026, 4, 17)
OUTPUT_PATH = os.path.expanduser("~/Desktop/Alon-Workspace/Docs/dashboard.html")

def notion_query(database_id, payload=None):
    cmd = ["curl", "-s", "-X", "POST",
        f"https://api.notion.com/v1/databases/{database_id}/query",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload or {"page_size": 100})]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def parse_tools(data):
    tools = []
    for page in data.get("results", []):
        p = page["properties"]
        tools.append({
            "name": "".join(t.get("plain_text", "") for t in p.get("Tool", {}).get("title", [])),
            "purpose": "".join(t.get("plain_text", "") for t in p.get("Purpose", {}).get("rich_text", [])),
            "connections": [o["name"] for o in p.get("Connections", {}).get("multi_select", [])],
            "integrated": p.get("Integrated", {}).get("checkbox", False),
            "core": (p.get("Core", {}).get("select") or {}).get("name", ""),
        })
    return tools

def parse_items(data):
    items = []
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
            "notes": "".join(t.get("plain_text", "") for t in p.get("Notes", {}).get("rich_text", [])),
            "categories": [o["name"] for o in p.get("Category", {}).get("multi_select", [])],
        })
    return items

def is_overdue(due_str):
    if not due_str: return False
    try: return date.fromisoformat(due_str) < date.today()
    except: return False

def fmt_due(due_str):
    if not due_str: return ""
    try: return date.fromisoformat(due_str).strftime("%b %d")
    except: return due_str

def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def dc(dept):
    return {"Marketing": "#EA4335", "Product": "#4285F4", "R&D": "#34A853"}.get(dept, "#888")

def cat_color(cat):
    return {"UI/UX": "#9334E9", "Creative Ads": "#EC4899", "R&D": "#3B82F6",
            "Content": "#22C55E", "YouTube": "#EF4444", "Business": "#EAB308",
            "Legal": "#6B7280", "Infrastructure": "#F97316"}.get(cat, "#888")

def cat_bg(cat):
    return {"UI/UX": "#F3E8FF", "Creative Ads": "#FCE7F3", "R&D": "#DBEAFE",
            "Content": "#DCFCE7", "YouTube": "#FEE2E2", "Business": "#FEF9C3",
            "Legal": "#F3F4F6", "Infrastructure": "#FFEDD5"}.get(cat, "#f0f0f0")

def dbg(dept):
    """Gentle pastel background + matching border for department-colored cards."""
    return {"Marketing": "background:#fef2f1;border-color:#f5c6c2",
            "Product": "background:#eef3fc;border-color:#c6dafc",
            "R&D": "background:#e6f4ea;border-color:#a8dab5"}.get(dept, "")

def dtc(dept):
    return {"Marketing": "tag-m", "Product": "tag-p", "R&D": "tag-r"}.get(dept, "")

def sc(status):
    return {"In Progress": "s-prog", "Done": "s-done", "Blocked": "s-block", "Not Started": "s-ns"}.get(status, "")

def generate_html(items, tools=None):
    today = date.today()
    id_map = {i["id"]: i for i in items}
    goals = [i for i in items if i["level"] == "Goal"]
    projects = [i for i in items if i["level"] == "Project"]
    tasks = [i for i in items if i["level"] == "Task"]
    all_active = [i for i in items if i["status"] != "Done"]
    overdue = [i for i in all_active if is_overdue(i["due"])]
    blocked = [i for i in all_active if i["status"] == "Blocked"]
    in_progress = [i for i in all_active if i["status"] == "In Progress"]
    not_started = [i for i in all_active if i["status"] == "Not Started"]
    days_to_launch = (LAUNCH_DATE - today).days
    overall_pct = int(sum(g["progress"] for g in goals) / max(len(goals), 1) * 100)
    tomorrow = today + timedelta(days=1)

    # Done today: items marked Done with due date today or earlier this week
    done_today = [i for i in items if i["status"] == "Done" and i["due"] and
        date.fromisoformat(i["due"]) == today]
    # Ahead of schedule: items due tomorrow (or later) but already Done
    done_ahead = [i for i in items if i["status"] == "Done" and i["due"] and
        date.fromisoformat(i["due"]) > today]

    # Week tasks
    week_tasks = sorted([t for t in tasks if t["status"] != "Done" and t["due"] and
        date.fromisoformat(t["due"]) <= today + timedelta(days=7)], key=lambda x: x["due"])
    days = {}
    for t in week_tasks:
        dk = date.fromisoformat(t["due"]).strftime("%a %d")
        days.setdefault(dk, []).append(t)

    # Team
    team = {}
    for i in all_active:
        team.setdefault(i["owner"] or "?", []).append(i)

    # Per-department stats
    dept_stats = {}
    for pn in ["Marketing", "Product", "R&D"]:
        pp = [p for p in projects if p["department"] == pn]
        pt = [t for t in tasks if t["department"] == pn]
        done_t = len([t for t in pt if t["status"] == "Done"])
        dept_stats[pn] = {"projects": len(pp), "tasks": len(pt), "done": done_t,
            "active": len([t for t in pt if t["status"] != "Done"]),
            "pct": int(sum(p["progress"] for p in pp) / max(len(pp), 1) * 100)}

    html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="60">
<title>VRT Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#eef0f4;color:#202124;padding:28px 48px;font-size:16px;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}}
.c{{margin:0}}

/* Header */
.hdr{{text-align:center;padding:20px 0 24px}}
.hdr h1{{font-size:clamp(36px,5vw,56px);font-weight:900;color:#202124;letter-spacing:-.5px}}
.hdr .sub{{color:#5f6368;font-size:15px;margin-top:8px;font-weight:500}}

/* Color utilities */
.ab{{color:#4285F4}}.ao{{color:#EA4335}}.ap{{color:#FBBC04}}.ag{{color:#34A853}}.ar{{color:#EA4335}}

/* ─── GROUP PANELS ─── wrap each section in a white container */
.group{{background:#fff;border-radius:16px;padding:24px;margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
.group-t{{font-size:22px;font-weight:900;margin-bottom:18px;color:#202124;display:flex;align-items:center;gap:10px}}
.group-t .group-badge{{font-size:12px;font-weight:700;color:#fff;padding:4px 12px;border-radius:20px;letter-spacing:.3px}}

/* Metrics strip — compact colored blocks */
.metrics{{display:flex;flex-wrap:wrap;gap:8px}}
.metric{{border-radius:10px;padding:8px 14px;display:flex;align-items:center;gap:8px;border:none}}
.metric .val{{font-size:22px;font-weight:900;line-height:1}}
.metric .lbl{{font-size:12px;text-transform:uppercase;letter-spacing:.5px;font-weight:700;opacity:.85}}
.m-blue{{background:#e8f0fe;color:#1967d2}}.m-green{{background:#e6f4ea;color:#137333}}.m-yellow{{background:#fef7e0;color:#e37400}}.m-red{{background:#fce8e6;color:#c5221f}}.m-dark{{background:#e8eaed;color:#3c4043}}

/* Alert */
.alert{{background:#fce8e6;border:1px solid #f5c6c2;border-radius:10px;padding:14px 18px;margin-bottom:20px;font-size:15px;color:#c5221f;font-weight:500}}
.alert b{{color:#EA4335}}

/* ─── TIER 1: Goals — hero cards ─── */
.goals{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.gc{{background:#f8f9fa;border-radius:14px;padding:20px;position:relative;overflow:hidden;border:1px solid #e8eaed;transition:border-color .15s,box-shadow .15s}}
.gc:hover{{border-color:#dadce0;box-shadow:0 4px 16px rgba(0,0,0,.08)}}
.gc::before{{content:'';position:absolute;top:0;left:0;right:0;height:5px}}
.gc.gc-m::before{{background:#EA4335}}.gc.gc-p::before{{background:#4285F4}}.gc.gc-r::before{{background:#34A853}}
.gc .gc-head{{margin-bottom:6px}}
.gc h3{{font-size:18px;font-weight:800;margin:0;color:#202124;line-height:1.3}}
.gc .gc-sub{{font-size:14px;color:#5f6368;margin-top:6px;line-height:1.5}}
.gc .gc-stats{{display:flex;gap:14px;margin-top:12px;font-size:13px;color:#80868b;font-weight:600}}
.gc .gc-stats span{{display:flex;align-items:center;gap:4px}}
.gc .gc-bar-row{{display:flex;align-items:center;gap:10px;margin-top:12px}}
.gc .gc-bar-row .pb{{flex:1;margin-top:0}}
.gc .gc-pct{{font-size:18px;font-weight:800;white-space:nowrap}}
.pb{{width:100%;height:6px;background:#e0e3e7;border-radius:3px;overflow:hidden;margin-top:12px}}
.pf{{height:100%;border-radius:3px}}

/* ─── TIER 2: Projects — board columns ─── */
.proj-board{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.proj-col{{background:#f8f9fa;border-radius:12px;padding:14px;border:1px solid #e8eaed}}
.proj-col-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;padding:12px 16px;border-radius:12px;background:#f1f3f4}}
.proj-col-head .pcol-title{{font-size:20px;font-weight:800;text-transform:uppercase;letter-spacing:.8px}}
.proj-col-head .pcol-count{{font-size:13px;color:#5f6368;font-weight:700;background:#e0e3e7;padding:3px 12px;border-radius:10px}}
.pc{{background:#fff;border:1px solid #e8eaed;border-radius:10px;padding:16px;margin-bottom:10px;transition:border-color .15s,box-shadow .15s}}
.pc:last-child{{margin-bottom:0}}
.pc:hover{{border-color:#c5c9cf;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.pc .pc-name{{font-size:15px;font-weight:700;margin-bottom:6px;color:#202124}}
.pc .pc-meta{{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:#5f6368}}
.pc .pc-bar{{margin-top:8px}}

/* ─── TIER 3: Tasks — kanban ─── */
.task-board{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}
.task-col{{background:#f8f9fa;border-radius:12px;padding:14px;border:1px solid #e8eaed}}
.task-col-head{{font-size:14px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid #e0e3e7;display:flex;justify-content:space-between;align-items:center}}
.task-col-head .col-count{{font-size:12px;font-weight:700;color:#5f6368;background:#e0e3e7;padding:2px 10px;border-radius:8px}}
.tk{{background:#fff;border:1px solid #e8eaed;border-radius:8px;padding:14px 16px;margin-bottom:8px;font-size:14px;transition:border-color .15s,box-shadow .15s}}
.tk:last-child{{margin-bottom:0}}
.tk:hover{{border-color:#c5c9cf;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.tk .tk-name{{font-weight:600;margin-bottom:5px;line-height:1.4;color:#202124}}
.tk .tk-foot{{display:flex;justify-content:space-between;font-size:12px;color:#5f6368;font-weight:500}}

/* Tags — bold, readable */
.tag{{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.3px;vertical-align:middle}}
.tag-m{{background:#fce8e6;color:#c5221f;border:1px solid #f5c6c2}}
.tag-p{{background:#e8f0fe;color:#1967d2;border:1px solid #c6dafc}}
.tag-r{{background:#e6f4ea;color:#137333;border:1px solid #a8dab5}}

/* Shared */
.own{{padding:3px 10px;background:#e8eaed;border-radius:6px;font-size:13px;font-weight:600;color:#3c4043}}
.s-prog{{color:#4285F4;font-weight:700}}.s-done{{color:#34A853;font-weight:700}}.s-block{{color:#EA4335;font-weight:700}}.s-ns{{color:#80868b;font-weight:600}}
.par{{font-size:10px;color:#80868b}}

/* Day grid */
.days{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}}
.dc{{background:#f8f9fa;border:1px solid #e8eaed;border-radius:10px;padding:14px}}
.dc.today{{border-color:#4285F4;border-width:2px;background:#e8f0fe}}
.dl{{font-size:13px;font-weight:800;color:#4285F4;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px}}
.dt{{font-size:14px;color:#3c4043;padding:6px 0;border-bottom:1px solid #e0e3e7;line-height:1.4}}
.dt:last-child{{border:0}}
.dt .dtowner{{font-size:10px;color:#80868b;font-weight:500}}

/* Team */
.tg{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.tc{{background:#f8f9fa;border:1px solid #e8eaed;border-radius:12px;padding:18px}}
.tc:hover{{border-color:#c5c9cf}}
.tc .tn{{font-size:20px;font-weight:800;margin-bottom:4px;color:#202124}}
.tc .tcnt{{font-size:13px;color:#5f6368;margin-bottom:10px;font-weight:600}}
.tc .ti{{font-size:14px;color:#3c4043;padding:6px 0;line-height:1.4;border-bottom:1px solid #e8eaed}}
.tc .ti:last-child{{border:0}}

/* Phase 0 Board */
.board-filters{{display:flex;gap:6px;margin-bottom:14px}}
.bf{{padding:6px 16px;border:1px solid #dadce0;border-radius:20px;background:#fff;font-size:12px;font-weight:600;cursor:pointer;transition:all .15s;font-family:inherit;color:#3c4043}}
.bf:hover{{background:#f1f3f4}}.bf.active{{background:#4285F4;color:#fff;border-color:#4285F4}}
.phase0-board{{display:flex;gap:8px;overflow-x:auto;padding-bottom:12px;-webkit-overflow-scrolling:touch}}
.p0-col{{min-width:160px;max-width:200px;flex-shrink:0;border-radius:12px;padding:10px;border:1px solid #e0e3e7}}
.p0-col-head{{font-size:13px;font-weight:800;text-align:center;padding-bottom:8px;border-bottom:2px solid rgba(0,0,0,.08);margin-bottom:8px;color:#3c4043}}
.p0-card{{background:#fff;border:1px solid #e0e3e7;border-radius:8px;padding:8px 10px;margin-bottom:6px;transition:box-shadow .15s}}
.p0-card:hover{{box-shadow:0 2px 8px rgba(0,0,0,.1)}}
.p0-card-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}}
.p0-card-name{{font-size:13px;font-weight:600;color:#202124;line-height:1.4;margin-bottom:4px}}
.p0-card-cats{{margin-bottom:4px}}
.cat-tag{{display:inline-block;padding:1px 6px;border-radius:8px;font-size:9px;font-weight:700;letter-spacing:.2px;border:1px solid rgba(0,0,0,.06)}}
.p0-card-foot{{display:flex;justify-content:space-between;align-items:center}}
.p0-owner{{font-size:10px;font-weight:600;color:#5f6368;background:#f1f3f4;padding:1px 8px;border-radius:6px}}
.p0-empty{{text-align:center;color:#c0c4c8;font-size:13px;padding:8px}}

/* ─── ROADMAP TIMELINE ─── */
.rm-wrap{{overflow-x:auto;-webkit-overflow-scrolling:touch}}
.rm-grid{{display:grid;gap:0;min-width:700px}}
.rm-phases{{display:flex;gap:2px;margin-bottom:6px}}
.rm-phase{{border-radius:8px;padding:6px 12px;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.5px;text-align:center;color:#fff}}
.rm-weeks{{display:flex;gap:0}}
.rm-wk{{flex:1;text-align:center;font-size:10px;font-weight:700;color:#80868b;padding:6px 0;border-right:1px solid #e8eaed;text-transform:uppercase;letter-spacing:.3px}}
.rm-wk.rm-wk-now{{background:#e8f0fe;color:#1967d2;border-radius:6px}}
.rm-lanes{{position:relative}}
.rm-row{{display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid #f1f3f4}}
.rm-row:last-child{{border:0}}
.rm-lbl{{width:140px;flex-shrink:0;font-size:12px;font-weight:600;color:#3c4043;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;cursor:pointer}}
.rm-track{{flex:1;position:relative;height:22px}}
.rm-bar{{position:absolute;height:18px;border-radius:9px;top:2px;display:flex;align-items:center;padding:0 6px;overflow:hidden;cursor:pointer;transition:opacity .15s}}
.rm-bar:hover{{opacity:.85}}
.rm-bar-fill{{position:absolute;top:0;left:0;height:100%;border-radius:9px;opacity:.3}}
.rm-bar-dots{{display:flex;gap:3px;position:relative;z-index:1}}
.rm-dot{{width:6px;height:6px;border-radius:50%;border:1px solid rgba(255,255,255,.6)}}
.rm-dot.done{{background:#fff}}.rm-dot.pending{{background:transparent}}.rm-dot.blocked{{background:#EA4335;border-color:#EA4335}}
.rm-today{{position:absolute;top:0;bottom:0;width:2px;background:#EA4335;z-index:5;pointer-events:none}}
.rm-today::after{{content:'TODAY';position:absolute;top:-16px;left:-16px;font-size:8px;font-weight:800;color:#EA4335;letter-spacing:.5px}}

/* Responsive */
@media(max-width:1024px){{body{{padding:20px 28px}}.group{{padding:20px}}}}
@media(max-width:900px){{.goals,.proj-board,.tg{{grid-template-columns:1fr}}.gc .gc-pct{{font-size:28px}}}}
@media(max-width:640px){{.days,.task-board{{grid-template-columns:1fr 1fr}}.tg{{grid-template-columns:1fr}}body{{padding:14px 16px}}.group{{padding:16px;border-radius:12px}}.hdr h1{{font-size:28px}}}}
@media(max-width:480px){{.task-board,.days{{grid-template-columns:1fr}}}}

.ts{{text-align:center;color:#9aa0a6;font-size:11px;padding:20px;font-weight:500}}

/* ─── NOTION SIDEBAR ─── */
.dash-wrap{{transition:margin-right .3s cubic-bezier(.4,0,.2,1)}}
body.sb-open .dash-wrap{{margin-right:380px}}
.sb{{position:fixed;top:0;right:-400px;width:380px;height:100vh;background:#fff;box-shadow:-4px 0 24px rgba(0,0,0,.1);z-index:1000;transition:right .3s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;overflow:hidden}}
body.sb-open .sb{{right:0}}
.sb-head{{padding:20px 20px 16px;border-bottom:1px solid #e8eaed;display:flex;justify-content:space-between;align-items:flex-start;flex-shrink:0}}
.sb-head h2{{font-size:16px;font-weight:800;color:#202124;line-height:1.3;flex:1;margin-right:12px}}
.sb-close{{width:28px;height:28px;border:none;background:#f1f3f4;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .15s}}
.sb-close:hover{{background:#e0e3e7}}
.sb-body{{flex:1;overflow-y:auto;padding:20px}}
.sb-row{{margin-bottom:14px}}
.sb-label{{font-size:10px;text-transform:uppercase;letter-spacing:.6px;font-weight:700;color:#80868b;margin-bottom:4px}}
.sb-val{{font-size:13px;color:#202124;font-weight:500;line-height:1.5}}
.sb-bar{{width:100%;height:8px;background:#e0e3e7;border-radius:4px;overflow:hidden;margin-top:6px}}
.sb-bar-fill{{height:100%;border-radius:4px;transition:width .4s ease}}
.sb-children{{list-style:none;padding:0}}
.sb-children li{{font-size:12px;color:#3c4043;padding:6px 10px;border-radius:6px;margin-bottom:4px;border:1px solid #e8eaed;cursor:pointer;transition:background .1s}}
.sb-children li:hover{{background:#f1f3f4}}
.sb-foot{{padding:16px 20px;border-top:1px solid #e8eaed;flex-shrink:0}}
.sb-notion{{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:10px;background:#202124;color:#fff;border:none;border-radius:10px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit;transition:background .15s;text-decoration:none}}
.sb-notion:hover{{background:#3c4043}}

/* Card Notion toggle icon */
.n-btn{{position:absolute;top:8px;right:8px;width:24px;height:24px;border:1px solid #dadce0;background:#fff;border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .15s,background .1s,border-color .1s;z-index:2}}
.n-btn:hover{{background:#f1f3f4;border-color:#c5c9cf}}
.n-btn.active{{opacity:1;background:#4285F4;border-color:#4285F4}}
.n-btn.active svg{{stroke:#fff}}
*:hover>.n-btn,*:hover .n-btn-wrap .n-btn{{opacity:1}}
.n-btn-wrap{{position:relative;display:inline}}

@media(max-width:900px){{.sb{{width:320px}}body.sb-open .dash-wrap{{margin-right:320px}}}}
@media(max-width:640px){{.sb{{width:100%;right:-100%}}body.sb-open .dash-wrap{{margin-right:0}}}}

/* ─── DRAG AND DROP ─── */
[draggable=true]{{cursor:grab;user-select:none}}
[draggable=true]:active{{cursor:grabbing}}
.dragging{{opacity:.4;transform:scale(.97);transition:opacity .15s,transform .15s}}
.drop-zone{{transition:background .2s,border-color .2s,box-shadow .2s}}
.drop-zone.drag-over{{background:#e8f0fe !important;border-color:#4285F4 !important;box-shadow:inset 0 0 0 2px #4285F4}}
.done-card.drag-over{{background:linear-gradient(135deg,#c8e6c9 0%,#a5d6a7 100%) !important;border-color:#2E7D32 !important;box-shadow:inset 0 0 0 2px #2E7D32}}
.drop-ghost{{height:4px;background:#4285F4;border-radius:2px;margin:4px 0;transition:all .15s}}
.drag-badge{{position:fixed;pointer-events:none;z-index:9999;background:#4285F4;color:#fff;padding:6px 14px;border-radius:8px;font-size:12px;font-weight:700;box-shadow:0 4px 12px rgba(0,0,0,.2);white-space:nowrap;max-width:260px;overflow:hidden;text-overflow:ellipsis}}
@keyframes drop-flash{{0%{{background:#e8f0fe}}100%{{background:transparent}}}}
.drop-flash{{animation:drop-flash .6s ease}}

/* ─── DONE FOR TODAY ─── */
.done-card{{background:linear-gradient(135deg,#e6f4ea 0%,#d4edda 100%);border:2px solid #34A853;border-radius:16px;padding:24px;margin-bottom:20px}}
.done-card .done-head{{font-size:22px;font-weight:900;color:#137333;margin-bottom:14px;display:flex;align-items:center;gap:10px}}
.done-card .done-list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}}
.done-item{{background:#fff;border:1px solid #34A85340;border-radius:10px;padding:12px 16px;display:flex;align-items:center;gap:10px;transition:box-shadow .15s}}
.done-item:hover{{box-shadow:0 2px 8px rgba(52,168,83,.15)}}
.done-item .done-check{{color:#34A853;font-size:18px;flex-shrink:0}}
.done-item .done-name{{font-size:14px;font-weight:600;color:#202124;flex:1}}
.done-item .done-meta{{font-size:11px;color:#5f6368;font-weight:500}}
.done-item .fire{{font-size:16px}}
.done-empty{{color:#34A853;font-size:15px;font-weight:600;opacity:.7}}

/* ─── LINKS PANEL ─── */
.links-panel{{background:#fff;border-radius:16px;margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,.06);overflow:hidden}}
.links-toggle{{width:100%;padding:16px 24px;background:#fff;border:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-family:inherit;font-size:18px;font-weight:800;color:#202124;transition:background .1s}}
.links-toggle:hover{{background:#f8f9fa}}
.links-toggle .lt-badge{{font-size:12px;font-weight:700;color:#fff;padding:3px 10px;border-radius:20px;background:#6C3AED}}
.links-toggle .lt-arr{{transition:transform .2s;font-size:14px;color:#5f6368}}
.links-body{{display:none;padding:0 24px 20px}}
.links-body.open{{display:block}}
.links-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}}
.lk-item{{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:8px;border:1px solid #e8eaed;text-decoration:none;color:#202124;font-size:13px;font-weight:600;transition:background .15s,border-color .15s}}
.lk-item:hover{{background:#f1f3f4;border-color:#dadce0}}
.lk-item .lk-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}}
.lk-item .lk-label{{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.lk-item .lk-ext{{font-size:10px;color:#80868b}}
.lk-cat{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#80868b;margin-bottom:6px;margin-top:12px;padding-left:4px}}
.lk-cat:first-child{{margin-top:0}}

/* ─── CHAT WINDOW ─── */
.chat-fab{{position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:#4285F4;border:none;cursor:pointer;box-shadow:0 4px 16px rgba(66,133,244,.4);z-index:900;display:flex;align-items:center;justify-content:center;transition:transform .2s,box-shadow .2s}}
.chat-fab:hover{{transform:scale(1.08);box-shadow:0 6px 24px rgba(66,133,244,.5)}}
.chat-fab svg{{pointer-events:none}}
.chat-win{{position:fixed;bottom:90px;right:24px;width:380px;max-height:500px;background:#fff;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,.15);z-index:900;display:none;flex-direction:column;overflow:hidden}}
.chat-win.open{{display:flex}}
.chat-hdr{{padding:14px 18px;background:#4285F4;color:#fff;display:flex;justify-content:space-between;align-items:center}}
.chat-hdr h3{{font-size:15px;font-weight:700;margin:0}}
.chat-hdr select{{background:rgba(255,255,255,.2);color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:8px;padding:4px 10px;font-size:12px;font-weight:600;font-family:inherit;cursor:pointer;outline:none}}
.chat-hdr select option{{color:#202124;background:#fff}}
.chat-msgs{{flex:1;overflow-y:auto;padding:14px;max-height:340px;min-height:120px}}
.chat-msg{{margin-bottom:10px;max-width:85%}}
.chat-msg.user{{margin-left:auto}}
.chat-msg.bot{{margin-right:auto}}
.chat-msg .chat-bubble{{padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.5;font-weight:500}}
.chat-msg.user .chat-bubble{{background:#e8f0fe;color:#1967d2;border-bottom-right-radius:4px}}
.chat-msg.bot .chat-bubble{{background:#f1f3f4;color:#3c4043;border-bottom-left-radius:4px}}
.chat-msg .chat-meta{{font-size:10px;color:#9aa0a6;margin-top:3px;font-weight:500}}
.chat-msg.user .chat-meta{{text-align:right}}
.chat-input{{display:flex;gap:8px;padding:12px 14px;border-top:1px solid #e8eaed}}
.chat-input input{{flex:1;border:1px solid #dadce0;border-radius:10px;padding:10px 14px;font-size:14px;font-family:inherit;outline:none;transition:border-color .15s}}
.chat-input input:focus{{border-color:#4285F4}}
.chat-input button{{background:#4285F4;color:#fff;border:none;border-radius:10px;padding:10px 16px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit;transition:background .15s;white-space:nowrap}}
.chat-input button:hover{{background:#1967d2}}
@media(max-width:480px){{.chat-win{{width:calc(100% - 32px);right:16px;bottom:80px}}.chat-fab{{bottom:16px;right:16px}}}}

/* ─── CARD SELECT & EXPAND ─── */
.gc,.pc,.tk{{cursor:pointer}}
.gc.selected,.pc.selected,.tk.selected{{outline:3px solid #6C3AED;outline-offset:-1px;z-index:10;position:relative}}
.gc.expanded{{grid-column:1/-1;transition:all .3s ease}}
.pc.expanded,.tk.expanded{{transition:all .3s ease}}
.sticky-tree{{margin-top:16px;padding-top:14px;border-top:2px solid #e0e3e7}}
.sticky-tree .st-label{{font-size:10px;text-transform:uppercase;letter-spacing:.6px;font-weight:700;color:#80868b;margin:10px 0 6px;padding-left:2px}}
.sticky-tree .st-label:first-child{{margin-top:0}}
.sticky{{padding:8px 12px;border-radius:8px;margin-bottom:4px;cursor:pointer;border:1px solid #e8eaed;background:#fff;display:flex;align-items:center;gap:8px;transition:background .15s,border-color .15s;font-size:13px;font-weight:500;color:#3c4043}}
.sticky:hover{{background:#f1f3f4;border-color:#dadce0}}
.sticky.current{{background:#e8f0fe;border:2px solid #4285F4;font-weight:700;color:#202124}}
.sticky.s-parent{{font-weight:700;border-color:#dadce0}}
.sticky .st-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}}
.sticky .st-name{{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.sticky .st-level{{font-size:9px;font-weight:700;text-transform:uppercase;padding:2px 6px;border-radius:6px;flex-shrink:0}}
.tool-card{{transition:opacity .3s ease}}
.tool-dimmed{{opacity:.15;pointer-events:none}}
</style></head>
<body>
<div class="sb" id="sb">
  <div class="sb-head"><h2 id="sb-title">—</h2><button class="sb-close" onclick="closePanel()"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2"><path d="M4 4l8 8M12 4l-8 8"/></svg></button></div>
  <div class="sb-body" id="sb-body"></div>
  <div class="sb-foot"><a class="sb-notion" id="sb-link" href="#" target="_blank"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2h8v8M14 2L6 10"/></svg>Open in Notion</a></div>
</div>
<div class="dash-wrap"><div class="c">

<div class="hdr">
  <h1 style="color:#5B21B6"><span style="color:#6C3AED">V</span><span style="color:#5B21B6">R</span><span style="color:#8B5CF6">T</span> Dashboard</h1>
  <div class="sub">{today.strftime("%A, %B %d")} &middot; {len(items)} items tracked &middot; Launch in {days_to_launch} days</div>
</div>

<div class="group" style="padding:16px 20px">
  <div class="metrics">
    <div class="metric m-blue"><div class="val">{days_to_launch}</div><div class="lbl">Days to {LAUNCH_DATE.strftime("%b %d")}</div></div>
    <div class="metric m-dark"><div class="val">{overall_pct}%</div><div class="lbl">Overall</div></div>
    <div class="metric m-green"><div class="val">{len(in_progress)}</div><div class="lbl">In Progress</div></div>
    <div class="metric m-yellow"><div class="val">{len(not_started)}</div><div class="lbl">Not Started</div></div>
    <div class="metric m-red"><div class="val">{len(overdue)}</div><div class="lbl">Overdue</div></div>
    <div class="metric m-red"><div class="val">{len(blocked)}</div><div class="lbl">Blocked</div></div>
    <div class="metric m-blue"><div class="val">{len(week_tasks)}</div><div class="lbl">This Week</div></div>
    <div class="metric m-dark"><div class="val">{len(all_active)}</div><div class="lbl">Active</div></div>
  </div>
</div>
"""

    # ═══ TIER 1: GOALS (BILLBOARD — INSPIRATION) ═══
    html += '<div class="group">\n<div class="group-t">Goals <span class="group-badge" style="background:#34A853">' + str(len(goals)) + ' departments</span></div>\n<div class="goals">\n'
    dept_cls = {"Marketing": "gc-m", "Product": "gc-p", "R&D": "gc-r"}
    for pn in ["Marketing", "Product", "R&D"]:
        for g in [x for x in goals if x["department"] == pn]:
            pct = int(g["progress"] * 100)
            children = [p for p in projects if g["id"] in p["parent_ids"]]
            s = dept_stats[pn]
            html += f"""  <div class="gc {dept_cls[pn]}" style="{dbg(pn)}" data-nid="{g["id"]}">
    <button class="n-btn" onclick="event.stopPropagation();openPanel('{g["id"]}')" title="Open in Notion"><svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2"><path d="M6 2h8v8M14 2L6 10"/></svg></button>
    <div class="gc-head"><span class="tag {dtc(pn)}">{esc(pn)}</span><h3 style="color:{dc(pn)};margin-top:6px">{esc(g["name"])}</h3></div>
    <div class="gc-sub">{esc(" / ".join(p["name"] for p in children[:4]))}</div>
    <div class="gc-bar-row"><div class="pb"><div class="pf" style="width:{pct}%;background:{dc(pn)}"></div></div><span class="gc-pct" style="color:{dc(pn)}">{pct}%</span></div>
    <div class="gc-stats"><span>{s['projects']} projects</span><span>{s['tasks']} tasks</span><span>{s['done']} done</span><span>Due {fmt_due(g["due"])}</span></div>
  </div>\n"""
    html += '</div></div>\n'

    # ═══ ROADMAP TIMELINE ═══
    rm_start = date(2026, 2, 18)
    rm_end = LAUNCH_DATE  # Apr 17
    rm_phases = [
        ("Foundation",    date(2026, 2, 18), date(2026, 3, 8),  "#4285F4"),
        ("Build Sprint",  date(2026, 3, 9),  date(2026, 3, 29), "#34A853"),
        ("Polish & Test", date(2026, 3, 30), date(2026, 4, 10), "#FBBC04"),
        ("Launch Prep",   date(2026, 4, 11), date(2026, 4, 16), "#EA4335"),
    ]
    total_days = (rm_end - rm_start).days + 1

    # Build week columns
    rm_weeks = []
    wk_start = rm_start
    while wk_start <= rm_end:
        wk_end = min(wk_start + timedelta(days=6), rm_end)
        rm_weeks.append((wk_start, wk_end))
        wk_start = wk_end + timedelta(days=1)

    # Active projects with scheduled child tasks
    rm_projects = []
    for p in projects:
        if p["status"] == "Done":
            continue
        child_tasks = [t for t in tasks if p["id"] in t["parent_ids"] and t["due"]]
        if not child_tasks:
            continue
        child_dues = [date.fromisoformat(t["due"]) for t in child_tasks]
        p_start = min(child_dues)
        p_end = max(child_dues)
        done_count = len([t for t in child_tasks if t["status"] == "Done"])
        blocked_count = len([t for t in child_tasks if t["status"] == "Blocked"])
        pending_count = len(child_tasks) - done_count - blocked_count
        rm_projects.append({
            "id": p["id"], "name": p["name"], "department": p["department"],
            "start": p_start, "end": p_end, "progress": p["progress"],
            "total": len(child_tasks), "done": done_count,
            "blocked": blocked_count, "pending": pending_count,
        })

    rm_projects.sort(key=lambda x: (x["start"], x["department"]))

    def day_pct(d):
        return max(0, min(100, ((d - rm_start).days / total_days) * 100))

    html += '<div class="group">\n'
    html += '<div class="group-t">Roadmap <span class="group-badge" style="background:#6C3AED">Feb 18 &rarr; Apr 17</span></div>\n'
    html += '<div class="rm-wrap">\n'

    # Phase bands
    html += '<div class="rm-phases">\n'
    for ph_name, ph_start, ph_end, ph_color in rm_phases:
        ph_days = (ph_end - ph_start).days + 1
        ph_width = (ph_days / total_days) * 100
        html += f'  <div class="rm-phase" style="background:{ph_color};width:{ph_width:.1f}%">{esc(ph_name)}</div>\n'
    html += '</div>\n'

    # Week headers
    html += '<div class="rm-weeks">\n'
    for wk_s, wk_e in rm_weeks:
        is_now = wk_s <= today <= wk_e
        cls = " rm-wk-now" if is_now else ""
        wk_days = (wk_e - wk_s).days + 1
        wk_width = (wk_days / total_days) * 100
        html += f'  <div class="rm-wk{cls}" style="width:{wk_width:.1f}%">{wk_s.strftime("%b %d")}</div>\n'
    html += '</div>\n'

    # Project lanes
    html += '<div class="rm-lanes" style="position:relative">\n'
    for rp in rm_projects:
        left = day_pct(rp["start"])
        right = day_pct(rp["end"] + timedelta(days=1))
        width = max(right - left, 2)
        color = dc(rp["department"])
        fill_pct = int(rp["progress"] * 100)

        # Task dots
        dots = ""
        for _ in range(rp["done"]):
            dots += '<span class="rm-dot done"></span>'
        for _ in range(rp["blocked"]):
            dots += '<span class="rm-dot blocked"></span>'
        for _ in range(min(rp["pending"], 8)):
            dots += '<span class="rm-dot pending"></span>'

        html += f'  <div class="rm-row">\n'
        html += f'    <div class="rm-lbl" onclick="openPanel(\'{rp["id"]}\')" title="{esc(rp["name"])}">'
        html += f'<span class="tag {dtc(rp["department"])}" style="font-size:8px;padding:1px 4px;margin-right:4px">{esc(rp["department"][:3])}</span>{esc(rp["name"][:20])}</div>\n'
        html += f'    <div class="rm-track">\n'
        html += f'      <div class="rm-bar" style="left:{left:.1f}%;width:{width:.1f}%;background:{color}" onclick="openPanel(\'{rp["id"]}\')">'
        html += f'<div class="rm-bar-fill" style="width:{fill_pct}%;background:#fff"></div>'
        html += f'<div class="rm-bar-dots">{dots}</div></div>\n'
        html += f'    </div>\n'
        html += f'  </div>\n'

    # Today marker
    today_pct = day_pct(today)
    if 0 < today_pct < 100:
        html += f'  <div class="rm-today" style="left:{today_pct:.1f}%"></div>\n'

    html += '</div>\n'  # rm-lanes
    html += '</div>\n'  # rm-wrap
    html += '</div>\n'  # group

    # ═══ DONE FOR TODAY ═══
    all_done_display = done_today + done_ahead
    if all_done_display:
        html += '<div class="done-card drop-zone" data-drop-status="Done">\n'
        html += '<div class="done-head"><span style="font-size:28px">&#10003;</span> Done for Today'
        if done_ahead:
            html += f' <span style="font-size:14px;font-weight:600;color:#e65100;background:#fff3e0;padding:3px 10px;border-radius:10px">{len(done_ahead)} ahead of schedule</span>'
        html += '</div>\n<div class="done-list">\n'
        for di in all_done_display:
            is_ahead = di in done_ahead
            fire = ' <span class="fire" title="Ahead of schedule!">&#128293;</span>' if is_ahead else ""
            level_lbl = di["level"]
            html += f'<div class="done-item" data-nid="{di["id"]}" style="position:relative">'
            html += f'<button class="n-btn" style="top:4px;right:4px;width:20px;height:20px;opacity:.6" onclick="event.stopPropagation();openPanel(\'{di["id"]}\')" title="Open in Notion"><svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2"><path d="M6 2h8v8M14 2L6 10"/></svg></button>'
            html += f'<span class="done-check">&#10003;</span>'
            html += f'<span class="done-name">{esc(di["name"])}{fire}</span>'
            html += f'<span class="done-meta"><span class="tag {dtc(di["department"])}" style="font-size:9px;padding:1px 6px">{esc(di["department"][:3])}</span> {esc(di["owner"])} &middot; {level_lbl}</span>'
            html += '</div>\n'
        html += '</div></div>\n'
    else:
        html += '<div class="done-card drop-zone" data-drop-status="Done" style="border-style:dashed;opacity:.6"><div class="done-head"><span style="font-size:28px">&#10003;</span> Done for Today</div><div class="done-empty">Nothing completed yet — drop items here!</div></div>\n'

    # Overdue alert
    if overdue:
        html += '<div class="alert"><b>&#9888; Overdue:</b> '
        html += ", ".join(f'{esc(o["name"])} ({fmt_due(o["due"])}, {esc(o["owner"])})' for o in overdue)
        html += '</div>\n'

    # ═══ TIER 2: PROJECTS (DATA MANAGEMENT) ═══
    html += '<div class="group">\n<div class="group-t">Projects <span class="group-badge" style="background:#4285F4">' + str(len(projects)) + ' active</span></div>\n<div class="proj-board">\n'
    for pn in ["Marketing", "Product", "R&D"]:
        pp = sorted([p for p in projects if p["department"] == pn], key=lambda x: x.get("due") or "z")
        html += f'  <div class="proj-col"><div class="proj-col-head"><span class="pcol-title" style="color:{dc(pn)}">{esc(pn)}</span><span class="pcol-count">{len(pp)}</span></div>\n'
        for p in pp:
            pct = int(p["progress"] * 100)
            od_cls = "ar" if is_overdue(p["due"]) else ""
            child_tasks = [t for t in tasks if p["id"] in t["parent_ids"]]
            done_ct = len([t for t in child_tasks if t["status"] == "Done"])
            total_ct = len(child_tasks)
            task_label = f"{done_ct}/{total_ct} tasks" if total_ct else "no tasks"
            html += f"""    <div class="pc" style="{dbg(pn)};position:relative" data-nid="{p["id"]}" draggable="true">
      <button class="n-btn" onclick="event.stopPropagation();openPanel('{p["id"]}')" title="Open in Notion"><svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2"><path d="M6 2h8v8M14 2L6 10"/></svg></button>
      <div class="pc-name">{esc(p["name"])}</div>
      <div class="pc-meta"><span class="own">{esc(p["owner"])}</span><span class="{sc(p["status"])}">{esc(p["status"])}</span></div>
      <div class="pc-meta" style="margin-top:4px"><span class="{od_cls}">{fmt_due(p["due"])}</span><span>{task_label}</span><span style="color:{dc(pn)};font-weight:700">{pct}%</span></div>
      <div class="pc-bar"><div class="pb"><div class="pf" style="width:{pct}%;background:{dc(pn)}"></div></div></div>
    </div>\n"""
        html += '  </div>\n'
    html += '</div></div>\n'

    # ═══ TIER 3: TASKS ═══
    active_tasks = [t for t in tasks if t["status"] != "Done"]
    status_order = [("In Progress", "ab", "#4285F4"), ("Not Started", "", "#80868b"), ("Blocked", "ar", "#EA4335")]
    done_tasks = [t for t in tasks if t["status"] == "Done"]

    html += '<div class="group">\n<div class="group-t">Tasks <span class="group-badge" style="background:#EA4335">' + str(len(active_tasks)) + ' active</span></div>\n<div class="task-board">\n'
    for st_name, st_cls, st_color in status_order:
        st_tasks = sorted([t for t in active_tasks if t["status"] == st_name], key=lambda x: x.get("due") or "z")
        html += f'  <div class="task-col drop-zone" data-drop-status="{st_name}"><div class="task-col-head"><span style="color:{st_color}">{esc(st_name)}</span><span class="col-count">{len(st_tasks)}</span></div>\n'
        for t in st_tasks:
            if is_overdue(t["due"]):
                card_style = "border-color:#EA433560;background:#fce8e6"
            else:
                card_style = dbg(t["department"])
            par = ""
            for pid in t["parent_ids"]:
                if pid in id_map: par = id_map[pid]["name"]
            html += f'    <div class="tk" style="{card_style};position:relative" data-nid="{t["id"]}" draggable="true"><button class="n-btn" onclick="event.stopPropagation();openPanel(\'{t["id"]}\')" title="Open in Notion"><svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2"><path d="M6 2h8v8M14 2L6 10"/></svg></button><div class="tk-name"><span class="tag {dtc(t["department"])}">{esc(t["department"][:3])}</span> {esc(t["name"])}</div>'
            html += f'<div class="tk-foot"><span class="own">{esc(t["owner"])}</span>'
            if par: html += f'<span class="par">{esc(par[:20])}</span>'
            od_c = "ar" if is_overdue(t["due"]) else ""
            html += f'<span class="{od_c}">{fmt_due(t["due"])}</span></div></div>\n'
        html += '  </div>\n'
    # Done column (collapsed)
    if done_tasks:
        html += f'  <div class="task-col" style="opacity:.6"><div class="task-col-head"><span class="ag">Done</span><span class="col-count">{len(done_tasks)}</span></div>\n'
        for t in done_tasks[:5]:
            html += f'    <div class="tk" style="border-color:#34A85330"><div class="tk-name" style="text-decoration:line-through;color:#9aa0a6"><span class="tag {dtc(t["department"])}" style="font-size:8px;padding:0 5px;opacity:.5">{esc(t["department"][:3])}</span> {esc(t["name"])}</div></div>\n'
        html += '  </div>\n'
    html += '</div></div>\n'

    # ═══ PHASE 0 BOARD ═══
    PHASE0_START = date(2026, 2, 18)
    PHASE0_END = date(2026, 3, 8)
    DAY_COLORS = ["#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#E0F7FA",
                  "#FBE9E7", "#E8EAF6", "#F1F8E9", "#FFF8E1", "#FCE4EC",
                  "#E0F2F1", "#FFF9C4", "#EDE9FE", "#E1F5FE", "#EFEBE9",
                  "#DBEAFE", "#D1FAE5", "#FEF3C7", "#FEE2E2"]

    phase0_tasks = [t for t in tasks if t["due"] and
        PHASE0_START <= date.fromisoformat(t["due"]) <= PHASE0_END]

    html += """<div class="group">
<div class="group-t">Phase 0 Board <span class="group-badge" style="background:#4285F4">Feb 18 – Mar 8</span></div>
<div class="board-filters">
  <button class="bf active" onclick="filterBoard('all')">All</button>
  <button class="bf" onclick="filterBoard('Alon')">Alon</button>
  <button class="bf" onclick="filterBoard('Matan')">Matan</button>
  <button class="bf" onclick="filterBoard('Sahar')">Sahar</button>
</div>
<div class="phase0-board">
"""
    for i in range(19):
        day = PHASE0_START + timedelta(days=i)
        day_str = day.isoformat()
        day_label = day.strftime("%a %b %d")
        bg = DAY_COLORS[i]
        is_today = day == today
        border = "border:3px solid #4285F4;" if is_today else ""
        today_badge = ' <span style="background:#4285F4;color:#fff;padding:1px 8px;border-radius:8px;font-size:10px;font-weight:700">TODAY</span>' if is_today else ""

        day_tasks = sorted([t for t in phase0_tasks if t["due"] == day_str],
                          key=lambda x: x["owner"])
        html += f'  <div class="p0-col drop-zone" data-drop-due="{day_str}" style="background:{bg};{border}">\n'
        html += f'    <div class="p0-col-head">{esc(day_label)}{today_badge}</div>\n'

        for t in day_tasks:
            cats_html = ""
            for cat in t.get("categories", []):
                cats_html += f'<span class="cat-tag" style="background:{cat_bg(cat)};color:{cat_color(cat)}">{esc(cat)}</span> '
            dept_tag = f'<span class="tag {dtc(t["department"])}" style="font-size:9px;padding:1px 6px">{esc(t["department"][:3])}</span>'
            owner_badge = f'<span class="p0-owner">{esc(t["owner"])}</span>'
            status_dot = ""
            if t["status"] == "Done":
                status_dot = '<span style="color:#34A853;font-size:14px" title="Done">&#10003;</span>'
            elif t["status"] == "In Progress":
                status_dot = '<span style="color:#4285F4;font-size:10px" title="In Progress">&#9679;</span>'
            elif t["status"] == "Blocked":
                status_dot = '<span style="color:#EA4335;font-size:10px" title="Blocked">&#9679;</span>'

            html += f'    <div class="p0-card" data-owner="{esc(t["owner"])}" data-nid="{t["id"]}" draggable="true" style="position:relative">\n'
            html += f'      <button class="n-btn" style="top:4px;right:4px;width:20px;height:20px" onclick="event.stopPropagation();openPanel(\'{t["id"]}\')" title="Open in Notion"><svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2"><path d="M6 2h8v8M14 2L6 10"/></svg></button>\n'
            html += f'      <div class="p0-card-top">{dept_tag} {status_dot}</div>\n'
            html += f'      <div class="p0-card-name">{esc(t["name"])}</div>\n'
            if cats_html:
                html += f'      <div class="p0-card-cats">{cats_html}</div>\n'
            html += f'      <div class="p0-card-foot">{owner_badge}</div>\n'
            html += f'    </div>\n'

        if not day_tasks:
            html += '    <div class="p0-empty">—</div>\n'

        html += '  </div>\n'

    html += '</div></div>\n'

    # ═══ THIS WEEK + TEAM side by side ═══
    # Daily breakdown
    if days:
        html += '<div class="group">\n<div class="group-t">This Week <span class="group-badge" style="background:#FBBC04;color:#202124">' + str(len(week_tasks)) + ' tasks</span></div>\n<div class="days">\n'
        for dk in sorted(days.keys()):
            is_td = dk == today.strftime("%a %d")
            cls = " today" if is_td else ""
            lbl = f"{dk} (today)" if is_td else dk
            html += f'  <div class="dc{cls}"><div class="dl">{esc(lbl)}</div>\n'
            for t in days[dk]:
                html += f'    <div class="dt" style="{dbg(t["department"])};border-radius:6px;padding:6px 8px;margin-bottom:4px;border-width:1px;border-style:solid"><span class="tag {dtc(t["department"])}">{esc(t["department"][:3])}</span> {esc(t["name"])}<br><span class="dtowner">{esc(t["owner"])}</span></div>\n'
            html += '  </div>\n'
        html += '</div></div>\n'

    # Team
    html += '<div class="group">\n<div class="group-t">Team <span class="group-badge" style="background:#202124">3 members</span></div>\n<div class="tg">\n'
    for member in ["Alon", "Matan", "Sahar"]:
        mi = [i for i in team.get(member, []) if i["status"] != "Done"]
        od_count = len([i for i in mi if is_overdue(i["due"])])
        od_badge = f' <span class="ar">({od_count} overdue)</span>' if od_count else ""
        html += f'  <div class="tc drop-zone" data-drop-owner="{member}"><div class="tn">{esc(member)}</div><div class="tcnt">{len(mi)} active{od_badge}</div>\n'
        for i in sorted(mi, key=lambda x: x.get("due") or "z")[:10]:
            od_m = " &#9888;" if is_overdue(i["due"]) else ""
            html += f'    <div class="ti" style="{dbg(i["department"])};border-radius:6px;padding:6px 8px;margin-bottom:3px;border-width:1px;border-style:solid"><span class="tag {dtc(i["department"])}">{esc(i["department"][:3])}</span> {esc(i["name"])}{od_m}</div>\n'
        html += '  </div>\n'
    html += '</div></div>\n'

    # ═══ TOOL STACK ═══
    if tools:
        core_tools = [t for t in tools if t["core"] == "CORE"]
        other_tools = [t for t in tools if t["core"] != "CORE"]
        integrated_count = len([t for t in tools if t["integrated"]])
        conn_colors = {
            "Notion": "#e8eaed", "Slack": "#e8f0fe", "Email": "#fef7e0", "Calendar": "#fff3e0",
            "Sites/Web": "#e6f4ea", "Payments": "#fce8e6", "CRM": "#f3e5f5", "Docs/Files": "#efebe9",
            "Automation": "#e8eaed", "Claude Code": "#fce4ec", "Code/Dev": "#e8f0fe",
            "Design": "#f3e5f5", "Social Media": "#fce4ec", "Hosting": "#e6f4ea", "AI/Generation": "#fff3e0"
        }
        conn_text = {
            "Notion": "#3c4043", "Slack": "#1967d2", "Email": "#e37400", "Calendar": "#e65100",
            "Sites/Web": "#137333", "Payments": "#c5221f", "CRM": "#7b1fa2", "Docs/Files": "#5d4037",
            "Automation": "#3c4043", "Claude Code": "#c2185b", "Code/Dev": "#1967d2",
            "Design": "#7b1fa2", "Social Media": "#c2185b", "Hosting": "#137333", "AI/Generation": "#e65100"
        }

        html += f'<div class="group" id="tool-stack-group">\n<div class="group-t" id="tool-stack-title">Tool Stack <span class="group-badge" style="background:#202124">{len(tools)} tools</span></div>\n'
        html += f'<div class="metrics" style="margin-bottom:16px">'
        html += f'<div class="metric m-blue"><div class="val">{len(core_tools)}</div><div class="lbl">Core</div></div>'
        html += f'<div class="metric m-green"><div class="val">{integrated_count}</div><div class="lbl">Integrated</div></div>'
        html += f'<div class="metric m-yellow"><div class="val">{len(tools) - integrated_count}</div><div class="lbl">Not Integrated</div></div>'
        html += f'</div>\n'

        html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px">\n'
        for t in core_tools + other_tools:
            border = "border:2px solid #FBBC04" if t["core"] == "CORE" else "border:1px solid #e8eaed"
            int_dot = '<span style="color:#34A853;font-size:12px" title="Integrated">&#9679;</span>' if t["integrated"] else '<span style="color:#dadce0;font-size:12px" title="Not integrated">&#9675;</span>'
            core_badge = ' <span style="background:#FEF7E0;color:#e37400;font-size:9px;font-weight:700;padding:1px 6px;border-radius:6px">CORE</span>' if t["core"] == "CORE" else ""
            conns_html = ""
            for c in t["connections"]:
                bg = conn_colors.get(c, "#f0f0f0")
                tc = conn_text.get(c, "#666")
                conns_html += f'<span style="display:inline-block;padding:1px 6px;border-radius:6px;font-size:9px;font-weight:600;background:{bg};color:{tc};margin:1px">{esc(c)}</span>'
            purpose_short = esc(t["purpose"][:60] + "..." if len(t["purpose"]) > 60 else t["purpose"])
            conns_str = ",".join(t["connections"])
            is_core = "true" if t["core"] == "CORE" else "false"
            html += f'  <div class="tool-card" data-connections="{conns_str}" data-core="{is_core}" style="background:#f8f9fa;{border};border-radius:10px;padding:12px;transition:box-shadow .15s" onmouseover="this.style.boxShadow=\'0 2px 8px rgba(0,0,0,.08)\'" onmouseout="this.style.boxShadow=\'none\'">\n'
            html += f'    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><span style="font-weight:700;font-size:13px;color:#202124">{esc(t["name"])}</span>{int_dot}</div>\n'
            html += f'    <div style="font-size:11px;color:#5f6368;margin-bottom:6px;line-height:1.4">{purpose_short}{core_badge}</div>\n'
            html += f'    <div>{conns_html}</div>\n'
            html += f'  </div>\n'
        html += '</div></div>\n'

    # ═══ LINKS PANEL ═══
    links_data = [
        ("Dashboards & Sites", "#6C3AED", [
            ("VRT Dashboard (live)", "https://vrt-dashboard.netlify.app", "#6C3AED"),
            ("Dashboard Server", "http://localhost:3001", "#4285F4"),
            ("VRT Domain", "https://vrt.co.il", "#34A853"),
        ]),
        ("Notion", "#000", [
            ("Workspace - VRT", "https://notion.so/30a5308b6bc580efae57e27dbfdfd1f2", "#000"),
            ("VRT Tracker DB", "https://notion.so/30a5308b6bc58171a2c3d89200293d13", "#000"),
            ("Feature Board DB", "https://notion.so/30a5308b6bc5814fba07d7ba33691adc", "#000"),
            ("Design Specs", "https://notion.so/30a5308b6bc58130aaddc1bd686dcc5e", "#000"),
            ("Tool Inventory DB", "https://notion.so/3408692eca1448868143-86ceb7f979e6", "#000"),
        ]),
        ("Dev Tools", "#4285F4", [
            ("GitHub", "https://github.com", "#333"),
            ("Netlify", "https://app.netlify.com", "#00C7B7"),
            ("Figma", "https://figma.com", "#A259FF"),
            ("Lovable", "https://lovable.dev", "#FF6B6B"),
        ]),
        ("Communication", "#EA4335", [
            ("Slack", "https://slack.com", "#4A154B"),
            ("Notion Calendar", "https://calendar.notion.so", "#000"),
        ]),
    ]
    link_count = sum(len(cat[2]) for cat in links_data)
    html += f'<div class="links-panel">\n'
    html += f'<button class="links-toggle" onclick="var b=this.nextElementSibling;b.classList.toggle(\'open\');this.querySelector(\'.lt-arr\').textContent=b.classList.contains(\'open\')?\'&#9650;\':\'&#9660;\'">'
    html += f'<span>&#128279; Links &amp; Resources <span class="lt-badge">{link_count}</span></span><span class="lt-arr">&#9660;</span></button>\n'
    html += '<div class="links-body">\n'
    for lk_cat_name, lk_cat_clr, lk_cat_links in links_data:
        html += f'<div class="lk-cat">{esc(lk_cat_name)}</div>\n<div class="links-grid">\n'
        for label, url, dot_color in lk_cat_links:
            html += f'<a class="lk-item" href="{url}" target="_blank"><span class="lk-dot" style="background:{dot_color}"></span><span class="lk-label">{esc(label)}</span><span class="lk-ext">&#8599;</span></a>\n'
        html += '</div>\n'
    html += '</div></div>\n'

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    html += f'<div class="ts">VRT Tracker &middot; {now} &middot; python3 Scripts/generate-dashboard.py to refresh</div>\n'
    # Serialize all items as JSON for sidebar lookups
    items_json = json.dumps({i["id"]: i for i in items}, ensure_ascii=False).replace("</", "<\\/")

    html += f"""<script>
var _items = {items_json};
var _activeId = null;

function openPanel(id) {{
  var item = _items[id];
  if (!item) return;
  // Toggle if same item
  if (_activeId === id) {{ closePanel(); return; }}
  _activeId = id;
  // Deactivate old buttons, activate new
  document.querySelectorAll('.n-btn.active').forEach(b => b.classList.remove('active'));
  var card = document.querySelector('[data-nid="'+id+'"]');
  if (card) {{ var btn = card.querySelector('.n-btn'); if(btn) btn.classList.add('active'); }}
  // Populate sidebar
  document.getElementById('sb-title').textContent = item.name;
  var nid = id.replace(/-/g, '');
  document.getElementById('sb-link').href = 'https://notion.so/' + nid;
  var colors = {{Marketing:'#EA4335', Product:'#4285F4'}};
  var c = colors[item.department] || '#888';
  var pct = Math.round((item.progress || 0) * 100);
  var body = '';
  // Meta row
  body += '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px">';
  if (item.level) body += '<span style="padding:3px 10px;border-radius:8px;font-size:11px;font-weight:700;background:#e8eaed;color:#3c4043">' + item.level + '</span>';
  if (item.department) body += '<span style="padding:3px 10px;border-radius:8px;font-size:11px;font-weight:700;background:' + (item.department==='Marketing'?'#fce8e6':'#e8f0fe') + ';color:' + c + '">' + item.department + '</span>';
  if (item.status) {{
    var sc = {{'In Progress':'#4285F4','Done':'#34A853','Blocked':'#EA4335','Not Started':'#80868b'}};
    body += '<span style="padding:3px 10px;border-radius:8px;font-size:11px;font-weight:700;color:' + (sc[item.status]||'#888') + ';border:1px solid ' + (sc[item.status]||'#888') + '30">' + item.status + '</span>';
  }}
  body += '</div>';
  // Progress
  body += '<div class="sb-row"><div class="sb-label">Progress</div><div style="display:flex;align-items:center;gap:10px"><div class="sb-bar"><div class="sb-bar-fill" style="width:'+pct+'%;background:'+c+'"></div></div><span style="font-size:14px;font-weight:800;color:'+c+'">'+pct+'%</span></div></div>';
  // Details
  if (item.owner) body += '<div class="sb-row"><div class="sb-label">Owner</div><div class="sb-val">' + item.owner + '</div></div>';
  if (item.due) body += '<div class="sb-row"><div class="sb-label">Due</div><div class="sb-val">' + item.due + '</div></div>';
  if (item.notes) body += '<div class="sb-row"><div class="sb-label">Notes</div><div class="sb-val" style="white-space:pre-wrap">' + item.notes.replace(/</g,'&lt;') + '</div></div>';
  // Children
  var children = Object.values(_items).filter(function(x) {{ return x.parent_ids && x.parent_ids.indexOf(id) !== -1; }});
  if (children.length) {{
    var childLevel = item.level === 'Goal' ? 'Projects' : 'Tasks';
    body += '<div class="sb-row"><div class="sb-label">' + childLevel + ' (' + children.length + ')</div><ul class="sb-children">';
    children.forEach(function(ch) {{
      var chpct = Math.round((ch.progress||0)*100);
      var sch = {{'In Progress':'#4285F4','Done':'#34A853','Blocked':'#EA4335','Not Started':'#ccc'}};
      var dot = '<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:' + (sch[ch.status]||'#ccc') + ';margin-right:6px"></span>';
      body += '<li onclick="openPanel(\\'' + ch.id + '\\')">' + dot + ch.name + ' <span style="float:right;font-size:10px;color:#80868b;font-weight:700">' + chpct + '%</span></li>';
    }});
    body += '</ul></div>';
  }}
  document.getElementById('sb-body').innerHTML = body;
  document.body.classList.add('sb-open');
}}

function closePanel() {{
  _activeId = null;
  document.body.classList.remove('sb-open');
  document.querySelectorAll('.n-btn.active').forEach(b => b.classList.remove('active'));
}}

// Close on Escape
document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') {{ closePanel(); if(typeof deselectAll==='function') deselectAll(); }} }});

function filterBoard(owner) {{
  document.querySelectorAll('.bf').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  document.querySelectorAll('.p0-card').forEach(card => {{
    if (owner === 'all' || card.dataset.owner === owner) {{
      card.style.display = '';
    }} else {{
      card.style.display = 'none';
    }}
  }});
}}
</script>
"""

    # ═══ CHAT WINDOW ═══
    html += """
<!-- Chat FAB -->
<button class="chat-fab" id="chatFab" onclick="toggleChat()" title="Team Chat">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
</button>

<!-- Chat Window -->
<div class="chat-win" id="chatWin">
  <div class="chat-hdr">
    <h3>VRT Chat</h3>
    <select id="chatUser">
      <option value="Alon">Alon</option>
      <option value="Matan">Matan</option>
      <option value="Sahar">Sahar</option>
    </select>
  </div>
  <div class="chat-msgs" id="chatMsgs">
    <div class="chat-msg bot"><div class="chat-bubble">Hey! Tell me what you got done. Example: "done with market research" or "started login PRD"</div></div>
  </div>
  <div class="chat-input">
    <input type="text" id="chatInput" placeholder="e.g. done with market research..." onkeydown="if(event.key==='Enter')sendChat()">
    <button onclick="sendChat()">Send</button>
  </div>
</div>

<script>
var _chatOpen = false;
function toggleChat() {
  _chatOpen = !_chatOpen;
  document.getElementById('chatWin').classList.toggle('open', _chatOpen);
  if (_chatOpen) document.getElementById('chatInput').focus();
}

function sendChat() {
  var input = document.getElementById('chatInput');
  var msg = input.value.trim();
  if (!msg) return;
  var user = document.getElementById('chatUser').value;
  input.value = '';

  // Add user message to UI
  addChatMsg(user, msg, 'user');

  // Send to server
  fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name: user, message: msg})
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    addChatMsg('VRT Bot', data.reply, 'bot');
    if (data.updated) {
      // Reload dashboard after a short delay to pick up regenerated HTML
      setTimeout(function() { location.reload(); }, 2000);
    }
  })
  .catch(function(err) {
    addChatMsg('VRT Bot', 'Could not reach the server. Make sure dashboard-server is running on port 3001.', 'bot');
  });
}

function addChatMsg(name, text, type) {
  var msgs = document.getElementById('chatMsgs');
  var now = new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
  var div = document.createElement('div');
  div.className = 'chat-msg ' + type;
  div.innerHTML = '<div class="chat-bubble">' + text.replace(/</g,'&lt;') + '</div><div class="chat-meta">' + name + ' &middot; ' + now + '</div>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

// Load chat history on open
(function() {
  fetch('/api/chat').then(function(r){return r.json()}).then(function(history) {
    history.forEach(function(m) {
      addChatMsg(m.name, m.message, m.type === 'bot' ? 'bot' : 'user');
    });
  }).catch(function(){});
})();

// ═══ DRAG AND DROP ═══
(function() {
  var dragId = null;
  var dragEl = null;

  // Tool icons per category
  var toolIcons = {
    'UI/UX': ['Figma','Lovable'],
    'R&D': ['GitHub','VS Code','Claude Code'],
    'Content': ['Google Drive','YouTube'],
    'YouTube': ['YouTube'],
    'Creative Ads': ['Midjourney','Figma'],
    'Business': ['Notion','Stripe'],
    'Legal': ['Notion','Google Drive'],
    'Infrastructure': ['GitHub','Netlify']
  };
  var toolColors = {
    'Figma':'#A259FF','Lovable':'#FF6B6B','GitHub':'#333','VS Code':'#007ACC',
    'Claude Code':'#D97706','Google Drive':'#4285F4','YouTube':'#FF0000',
    'Midjourney':'#0D1117','Notion':'#000','Stripe':'#635BFF','Netlify':'#00C7B7'
  };

  // Show tool icons in sidebar when panel opens
  var origOpenPanel = window.openPanel;
  window.openPanel = function(id) {
    origOpenPanel(id);
    var item = _items[id];
    if (!item) return;
    // Build tool strip
    var cats = item.categories || [];
    var tools = [];
    cats.forEach(function(c) { (toolIcons[c]||[]).forEach(function(t){ if(tools.indexOf(t)===-1) tools.push(t); }); });
    if (!tools.length) tools = ['Notion']; // fallback
    var strip = document.getElementById('sb-tools');
    if (!strip) {
      strip = document.createElement('div');
      strip.id = 'sb-tools';
      strip.style.cssText = 'display:flex;gap:6px;flex-wrap:wrap;padding:12px 20px 0;border-top:1px solid #e8eaed';
      var sbBody = document.getElementById('sb-body');
      sbBody.parentNode.insertBefore(strip, sbBody);
    }
    strip.innerHTML = tools.map(function(t) {
      var c = toolColors[t]||'#888';
      return '<span style="padding:4px 10px;border-radius:8px;font-size:11px;font-weight:700;background:'+c+'18;color:'+c+';border:1px solid '+c+'30">'+t+'</span>';
    }).join('');
  };

  // Event delegation for drag start
  document.addEventListener('dragstart', function(e) {
    var card = e.target.closest('[data-nid][draggable]');
    if (!card) return;
    dragId = card.dataset.nid;
    dragEl = card;
    window._lastDrag = Date.now();
    card.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', dragId);
    // Highlight all drop zones
    document.querySelectorAll('.drop-zone').forEach(function(z) {
      z.style.outline = '2px dashed #4285F440';
      z.style.outlineOffset = '-2px';
    });
  });

  document.addEventListener('dragend', function(e) {
    if (dragEl) dragEl.classList.remove('dragging');
    dragId = null;
    dragEl = null;
    document.querySelectorAll('.drop-zone').forEach(function(z) {
      z.classList.remove('drag-over');
      z.style.outline = '';
      z.style.outlineOffset = '';
    });
  });

  document.addEventListener('dragover', function(e) {
    var zone = e.target.closest('.drop-zone');
    if (!zone || !dragId) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    // Clear other highlights
    document.querySelectorAll('.drop-zone.drag-over').forEach(function(z) { z.classList.remove('drag-over'); });
    zone.classList.add('drag-over');
  });

  document.addEventListener('dragleave', function(e) {
    var zone = e.target.closest('.drop-zone');
    if (zone) zone.classList.remove('drag-over');
  });

  document.addEventListener('drop', function(e) {
    e.preventDefault();
    var zone = e.target.closest('.drop-zone');
    if (!zone || !dragId) return;
    zone.classList.remove('drag-over');

    var updates = {};
    // Determine what changed based on drop zone attributes
    if (zone.dataset.dropStatus) {
      updates.status = zone.dataset.dropStatus;
    }
    if (zone.dataset.dropOwner) {
      updates.owner = zone.dataset.dropOwner;
    }
    if (zone.dataset.dropDue) {
      updates.due = zone.dataset.dropDue;
    }

    if (!Object.keys(updates).length) return;

    // Optimistic UI: move card visually
    if (dragEl) {
      dragEl.classList.add('drop-flash');
      if (updates.status === 'Done') {
        dragEl.style.opacity = '.5';
        dragEl.style.textDecoration = 'line-through';
      }
    }

    // Send to server
    fetch('/api/move', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({pageId: dragId, updates: updates})
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.success) {
        // Show success toast
        showToast('Moved: ' + (updates.status || updates.owner || updates.due));
        // Reload after regen
        setTimeout(function() { location.reload(); }, 2500);
      } else {
        showToast('Error: ' + (data.error || 'unknown'), true);
      }
    })
    .catch(function() {
      showToast('Server offline — start dashboard-server', true);
    });
  });

  // Toast notification
  function showToast(msg, isError) {
    var t = document.createElement('div');
    t.style.cssText = 'position:fixed;bottom:90px;left:50%;transform:translateX(-50%);padding:10px 24px;border-radius:10px;font-size:14px;font-weight:600;z-index:9999;box-shadow:0 4px 16px rgba(0,0,0,.15);transition:opacity .3s;font-family:Inter,sans-serif;';
    t.style.background = isError ? '#fce8e6' : '#e6f4ea';
    t.style.color = isError ? '#c5221f' : '#137333';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function() { t.style.opacity = '0'; }, 2000);
    setTimeout(function() { t.remove(); }, 2500);
  }

  // Touch support for mobile drag
  var touchDragId = null;
  document.addEventListener('touchstart', function(e) {
    var card = e.target.closest('[data-nid][draggable]');
    if (card) touchDragId = card.dataset.nid;
  }, {passive: true});
  document.addEventListener('touchend', function(e) {
    if (!touchDragId) return;
    var touch = e.changedTouches[0];
    var el = document.elementFromPoint(touch.clientX, touch.clientY);
    var zone = el ? el.closest('.drop-zone') : null;
    if (zone && zone.dataset.dropStatus) {
      fetch('/api/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({pageId: touchDragId, updates: {status: zone.dataset.dropStatus}})
      }).then(function() { setTimeout(function(){ location.reload(); }, 2000); });
    }
    touchDragId = null;
  });
})();
</script>
"""

    # ═══ CARD SELECT & EXPAND ═══
    html += """<script>
var _selectedId = null;
var _catToConn = {
  'UI/UX': ['Design','Sites/Web'],
  'R&D': ['Code/Dev','Automation'],
  'Content': ['Docs/Files','Sites/Web'],
  'Creative Ads': ['Design','AI/Generation'],
  'YouTube': ['Social Media','Sites/Web'],
  'Business': ['Docs/Files','Automation'],
  'Legal': ['Docs/Files'],
  'Infrastructure': ['Code/Dev','Automation','Hosting']
};

function selectCard(id) {
  var card = document.querySelector('[data-nid="'+id+'"]');
  if (!card || card.classList.contains('dragging')) return;
  if (id === _selectedId) { deselectAll(); return; }
  deselectAll(true);
  _selectedId = id;
  card.classList.add('selected','expanded');
  var tree = buildStickyTree(id);
  if (tree) card.appendChild(tree);
  filterToolStack(id);
}

function deselectAll(silent) {
  _selectedId = null;
  document.querySelectorAll('.selected,.expanded').forEach(function(el) {
    el.classList.remove('selected','expanded');
  });
  document.querySelectorAll('.sticky-tree').forEach(function(el) { el.remove(); });
  if (!silent) {
    document.querySelectorAll('.tool-card').forEach(function(el) { el.classList.remove('tool-dimmed'); });
    var tTitle = document.getElementById('tool-stack-title');
    if (tTitle) {
      var tc = document.querySelectorAll('.tool-card').length;
      tTitle.innerHTML = 'Tool Stack <span class="group-badge" style="background:#202124">' + tc + ' tools</span>';
    }
  }
}

function buildStickyTree(id) {
  var item = _items[id];
  if (!item) return null;
  var container = document.createElement('div');
  container.className = 'sticky-tree';
  var sc = {'In Progress':'#4285F4','Done':'#34A853','Blocked':'#EA4335','Not Started':'#ccc'};
  var lc = {'Goal':'#34A853','Project':'#4285F4','Task':'#EA4335'};

  function mkSticky(it, isCur, isPar) {
    var s = document.createElement('div');
    s.className = 'sticky' + (isCur ? ' current' : '') + (isPar ? ' s-parent' : '');
    s.setAttribute('data-page-id', it.id);
    var dot = '<span class="st-dot" style="background:'+(sc[it.status]||'#ccc')+'"></span>';
    var lvl = '<span class="st-level" style="background:'+(lc[it.level]||'#e8eaed')+'18;color:'+(lc[it.level]||'#5f6368')+'">'+(it.level||'')+'</span>';
    var nm = '<span class="st-name">'+(it.name||'').replace(/</g,'&lt;')+'</span>';
    s.innerHTML = dot + nm + lvl;
    if (!isCur) s.onclick = function(e) { e.stopPropagation(); navigateToItem(it.id); };
    return s;
  }

  // Walk up the parent chain
  var parents = [];
  var cur = item;
  while (cur.parent_ids && cur.parent_ids.length) {
    var pid = cur.parent_ids[0];
    var par = _items[pid];
    if (!par) break;
    parents.unshift(par);
    cur = par;
  }

  // Render parent chain
  parents.forEach(function(p) {
    var lb = document.createElement('div');
    lb.className = 'st-label';
    lb.textContent = p.level;
    container.appendChild(lb);
    container.appendChild(mkSticky(p, false, true));
  });

  // Find siblings (same parent, same level)
  var siblings = [];
  if (item.parent_ids && item.parent_ids.length) {
    var parentId = item.parent_ids[0];
    siblings = Object.values(_items).filter(function(x) {
      return x.parent_ids && x.parent_ids.indexOf(parentId) !== -1 && x.level === item.level;
    });
  }

  // Render siblings section (includes self, highlighted)
  if (siblings.length > 0) {
    var lb = document.createElement('div');
    lb.className = 'st-label';
    lb.textContent = item.level + 's';
    container.appendChild(lb);
    siblings.forEach(function(sib) {
      container.appendChild(mkSticky(sib, sib.id === id, false));
    });
  } else {
    container.appendChild(mkSticky(item, true, false));
  }

  // Find children
  var children = Object.values(_items).filter(function(x) {
    return x.parent_ids && x.parent_ids.indexOf(id) !== -1;
  });
  if (children.length) {
    var childLvl = item.level === 'Goal' ? 'Projects' : 'Tasks';
    var lb = document.createElement('div');
    lb.className = 'st-label';
    lb.textContent = childLvl;
    container.appendChild(lb);
    children.forEach(function(ch) {
      container.appendChild(mkSticky(ch, false, false));
    });
  }

  return container;
}

function filterToolStack(id) {
  var item = _items[id];
  if (!item) return;
  var cats = item.categories || [];
  var relevant = {};
  cats.forEach(function(c) {
    (_catToConn[c]||[]).forEach(function(conn) { relevant[conn] = true; });
  });
  var hasRelevant = Object.keys(relevant).length > 0;

  document.querySelectorAll('.tool-card').forEach(function(tc) {
    var conns = (tc.dataset.connections || '').split(',');
    var isCore = tc.dataset.core === 'true';
    var match = isCore;
    if (hasRelevant && !match) {
      conns.forEach(function(c) { if (relevant[c]) match = true; });
    }
    if (!hasRelevant) match = true;
    tc.classList.toggle('tool-dimmed', !match);
  });

  var tTitle = document.getElementById('tool-stack-title');
  if (tTitle) {
    var shown = document.querySelectorAll('.tool-card:not(.tool-dimmed)').length;
    tTitle.innerHTML = 'Tools for <span style="color:#6C3AED">' + (item.name||'').replace(/</g,'&lt;') + '</span> <span class="group-badge" style="background:#6C3AED">' + shown + ' relevant</span>';
  }
}

function navigateToItem(id) {
  deselectAll();
  var card = document.querySelector('[data-nid="'+id+'"]');
  if (!card) return;
  card.scrollIntoView({ behavior: 'smooth', block: 'center' });
  setTimeout(function() { selectCard(id); }, 500);
}

// Card click handler via event delegation
document.addEventListener('click', function(e) {
  if (e.target.closest('.n-btn')) return;
  if (e.target.closest('.sb')) return;
  if (e.target.closest('.sticky')) return;
  var card = e.target.closest('.gc[data-nid], .pc[data-nid], .tk[data-nid]');
  if (card) {
    if (window._lastDrag && Date.now() - window._lastDrag < 300) return;
    selectCard(card.dataset.nid);
    return;
  }
  if (_selectedId && !e.target.closest('.tool-card, .sticky-tree')) {
    deselectAll();
  }
});
</script>
"""

    html += '</div></div></body></html>'
    return html


if __name__ == "__main__":
    print("Pulling VRT Tracker...")
    data = notion_query(TRACKER_DB)
    items = parse_items(data)
    while data.get("has_more"):
        data = notion_query(TRACKER_DB, {"page_size": 100, "start_cursor": data["next_cursor"]})
        items.extend(parse_items(data))
    print(f"{len(items)} tracker items.")

    print("Pulling Tool Inventory...")
    tool_data = notion_query(TOOL_INV_DB)
    tools = parse_tools(tool_data)
    print(f"{len(tools)} tools.")

    print("Generating dashboard...")
    html = generate_html(items, tools)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)
    # Also write index.html for Netlify
    index_path = os.path.join(os.path.dirname(OUTPUT_PATH), "index.html")
    with open(index_path, "w") as f:
        f.write(html)
    print(f"Written to {OUTPUT_PATH} + index.html")
    # Only open in browser if run directly (not via server regen)
    if os.environ.get("VRT_NO_OPEN") != "1":
        subprocess.run(["open", OUTPUT_PATH])
