"""
Reorganize Notion: create a Master Map page and move all root-level items under it.
Then populate the master page with a full hierarchy overview.
"""

import requests
import time
import os

API_KEY = os.environ.get("NOTION_API_KEY", "")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
BASE = "https://api.notion.com/v1"

# ── Helpers ──────────────────────────────────────────────────────────────────

def rt(content, bold=False, italic=False, code=False, color=None, link=None):
    obj = {"type": "text", "text": {"content": content}}
    if link:
        obj["text"]["link"] = {"url": link}
    annot = {}
    if bold: annot["bold"] = True
    if italic: annot["italic"] = True
    if code: annot["code"] = True
    if color: annot["color"] = color
    if annot:
        obj["annotations"] = annot
    return obj


def heading(level, text):
    return {"object": "block", "type": f"heading_{level}",
            f"heading_{level}": {"rich_text": [rt(text)]}}


def paragraph(*parts):
    if len(parts) == 1 and isinstance(parts[0], str):
        rich = [rt(parts[0])]
    elif len(parts) == 1 and isinstance(parts[0], list):
        rich = parts[0]
    elif len(parts) == 1 and isinstance(parts[0], dict):
        rich = [parts[0]]
    else:
        rich = list(parts)
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}}


def bulleted(text_or_parts):
    if isinstance(text_or_parts, str):
        rich = [rt(text_or_parts)]
    else:
        rich = list(text_or_parts)
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rich}}


def callout(text, emoji="📌"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [rt(text)],
                        "icon": {"type": "emoji", "emoji": emoji}}}


def divider():
    return {"object": "block", "type": "divider", "divider": {}}


def empty():
    return paragraph("")


def notion_link(page_id):
    """Return a Notion page URL."""
    clean = page_id.replace("-", "")
    return f"https://www.notion.so/{clean}"


# ── API ──────────────────────────────────────────────────────────────────────

def create_page(title, parent_type="workspace", parent_id=None, icon=None):
    body = {
        "parent": {"workspace": True} if parent_type == "workspace"
                  else {"page_id": parent_id},
        "properties": {
            "title": [{"text": {"content": title}}]
        },
    }
    if icon:
        body["icon"] = {"type": "emoji", "emoji": icon}
    r = requests.post(f"{BASE}/pages", headers=HEADERS, json=body)
    if r.status_code == 200:
        pid = r.json()["id"]
        print(f"  Created page '{title}' -> {pid}")
        return pid
    else:
        print(f"  FAILED to create '{title}': {r.status_code} {r.text[:200]}")
        return None


def move_page(page_id, new_parent_id, title=""):
    r = requests.patch(f"{BASE}/pages/{page_id}", headers=HEADERS,
                       json={"parent": {"page_id": new_parent_id}})
    if r.status_code == 200:
        print(f"  Moved page '{title}' -> under master")
    else:
        print(f"  FAILED to move '{title}': {r.status_code} {r.text[:150]}")
    time.sleep(0.35)
    return r.status_code == 200


def move_database(db_id, new_parent_id, title=""):
    r = requests.patch(f"{BASE}/databases/{db_id}", headers=HEADERS,
                       json={"parent": {"page_id": new_parent_id}})
    if r.status_code == 200:
        print(f"  Moved database '{title}' -> under master")
    else:
        print(f"  FAILED to move DB '{title}': {r.status_code} {r.text[:150]}")
    time.sleep(0.35)
    return r.status_code == 200


def archive_page(page_id, title=""):
    r = requests.patch(f"{BASE}/pages/{page_id}", headers=HEADERS,
                       json={"archived": True})
    if r.status_code == 200:
        print(f"  Archived page '{title}'")
    else:
        print(f"  FAILED to archive '{title}': {r.status_code} {r.text[:150]}")
    return r.status_code == 200


def append_blocks(page_id, blocks):
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        r = requests.patch(f"{BASE}/blocks/{page_id}/children",
                           headers=HEADERS, json={"children": batch})
        if r.status_code == 200:
            print(f"  Appended {len(batch)} blocks")
        else:
            print(f"  FAILED append: {r.status_code} {r.text[:200]}")
            return False
    return True


# ── IDs ──────────────────────────────────────────────────────────────────────

WORKSPACE = "9a0ef9f8-e383-4a28-8a12-ba27fc0697cf"
VRT_PAGE = "30a5308b-6bc5-80ef-ae57-e27dbfdfd1f2"
TODO_DB = "1b0b2577-f110-4291-bf97-7e4b4b1c7d8d"
LIFE = "8a97027d-e2d4-45b9-9b66-a5e180582ce6"
DOCS_ALL = "3085308b-6bc5-8008-b331-d36ee0020256"
WORKSPACE_CLAUDE = "30a5308b-6bc5-805f-92cd-c7a29968bc7d"
PAGE_C = "30a5308b-6bc5-80dd-be33-f8ef3ee23218"


# ── Master page content ─────────────────────────────────────────────────────

def master_content():
    return [
        callout(
            "Your entire Notion workspace in one place. Every page, database, "
            "and how they connect — all mapped out below.",
            "🗺️"
        ),
        paragraph([
            rt("Last reorganized: "),
            rt("Feb 17, 2026", bold=True),
            rt(" — by Claude Code"),
        ]),
        empty(),
        divider(),

        # ── Work / VRT section ──
        heading(1, "Work"),
        empty(),

        heading(2, "Workspace Hub"),
        paragraph([
            rt("Your central workspace with tools, workflow, and Claude Code integration. "),
            rt("→ Open Workspace", bold=True, link=notion_link(WORKSPACE)),
        ]),
        bulleted([
            rt("Workspace - VRT", bold=True, link=notion_link(VRT_PAGE)),
            rt(" — VRT-specific workspace (team, workflow, local paths)"),
        ]),
        bulleted([rt("Tool Inventory databases (inside both workspace pages)")]),
        empty(),

        heading(2, "To-Do"),
        paragraph([
            rt("Your task tracker. All tasks, learning items, and action items live here. "),
            rt("→ Open To-Do", bold=True, link=notion_link(TODO_DB)),
        ]),
        paragraph([rt("Active/recent tasks:", italic=True)]),
        bulleted("Zoom out - breaths"),
        bulleted("Learning Claude"),
        bulleted("MVP - Design"),
        bulleted("MVP Deep work"),
        bulleted("Weekly Flow Full & Tools"),
        bulleted("Implementation of Claude and trials"),
        bulleted("Debugger research"),
        bulleted([rt("...and ", italic=True), rt("~30 more tasks", italic=True)]),
        empty(),

        heading(2, "Docs"),
        paragraph([
            rt("Documentation hub. "),
            rt("→ Open DOCS.all", bold=True, link=notion_link(DOCS_ALL)),
        ]),
        bulleted([
            rt("Product Management", bold=True),
            rt(" → PM DOCS → MVP Overview"),
        ]),
        bulleted("Slack Weekly Template"),
        bulleted("Miki AI"),
        empty(),

        divider(),

        # ── Personal section ──
        heading(1, "Personal"),
        empty(),

        heading(2, "Life"),
        paragraph([
            rt("Personal space — ideas, music, memories. "),
            rt("→ Open Life", bold=True, link=notion_link(LIFE)),
        ]),
        bulleted([
            rt("Ideas and..", bold=True),
            rt(" — invention ideas, creative concepts, רעיונות database"),
        ]),
        bulleted([
            rt("music", bold=True),
            rt(" — music notes"),
        ]),
        bulleted([
            rt("Dump", bold=True),
            rt(" — quick notes dump"),
        ]),
        bulleted([
            rt("things i wanna remember", bold=True),
        ]),
        bulleted([
            rt("OldStuff", bold=True, italic=True),
            rt(" (nested deeper) — graphic design, music production, journal, reading list, personal development, song lyrics"),
        ]),
        empty(),

        divider(),

        # ── Archived / Cleanup ──
        heading(1, "Cleaned up"),
        paragraph([
            rt("These empty pages were archived during reorganization:", italic=True),
        ]),
        bulleted([rt("Workspace.Claude", italic=True), rt(" — was empty, Claude Code info now lives in the Workspace page")]),
        bulleted([rt("c", italic=True), rt(" — empty test page")]),
        empty(),

        divider(),

        # ── Full tree ──
        heading(1, "Full page tree"),
        paragraph("Complete hierarchy of every page and database in this Notion workspace:"),
        empty(),

        # Workspace tree
        heading(3, "🪄 Workspace"),
        bulleted("Workspace - VRT"),
        bulleted("  └ Tool Inventory DB (Claude Code, Figma, Google Drive, Notion, Notion Calendar, Slack, VS Code)"),
        bulleted("  └ Tool Inventory DB (parent workspace)"),
        bulleted("  └ Replacement DB"),
        empty(),

        # To-Do tree
        heading(3, "📋 To-Do (database)"),
        paragraph("~30 task items including:"),
        bulleted("VRT tasks: MVP Design, MVP Deep work, Tasks MVP, cubes → MVP Phase 1"),
        bulleted("Learning: Claude, SQL, npm, internet, debugger research"),
        bulleted("Workflow: weekly flow, weekly template, Assembly line visual"),
        bulleted("Personal: muffins, לערוך סרטונים של אמא, סרטון יוטיוב, לקרוא את הספר"),
        empty(),

        # Docs tree
        heading(3, "📄 DOCS.all"),
        bulleted("Product Management → PM DOCS → MVP Overview"),
        bulleted("Slack Weekly Template"),
        bulleted("Miki AI"),
        empty(),

        # Life tree
        heading(3, "🏠 Life"),
        bulleted("Ideas and.. → רעיונות DB, invention ideas, creative concepts"),
        bulleted("music"),
        bulleted("Dump"),
        bulleted("things i wanna remember"),
        bulleted("OldStuff (nested) → graphic design (UI/UX learning, Knowledge & Resources DB), music production (שירים, songs list DB, plugins), Journal, scars of gods, Reading List (Books list, Media DB), Personal Development DB, The book of my best thoughts"),
        empty(),

        divider(),
        paragraph([
            rt("This map is maintained by Claude Code. ", italic=True),
            rt("Ask Claude to update it when you add or move pages.", italic=True),
        ]),
    ]


# ── Main ─────────────────────────────────────────────────────────────────────

def run():
    # Can't create at workspace root via API, so use Workspace as the root hub.
    # Create "Notion Master Map" as a child page of Workspace.
    master_parent = WORKSPACE  # 🪄 Workspace is our root

    # Step 1: Archive empty pages
    print("=" * 60)
    print("STEP 1: Archive empty pages")
    print("=" * 60)
    archive_page(WORKSPACE_CLAUDE, "Workspace.Claude")
    archive_page(PAGE_C, "c")
    print()

    # Step 2: Move root-level items under Workspace
    print("=" * 60)
    print("STEP 2: Move root-level items under Workspace")
    print("=" * 60)
    move_page(LIFE, master_parent, "Life")
    move_page(DOCS_ALL, master_parent, "DOCS.all")
    move_database(TODO_DB, master_parent, "To-Do")
    print()

    # Step 3: Create "Notion Master Map" child page under Workspace
    print("=" * 60)
    print("STEP 3: Create Notion Master Map page")
    print("=" * 60)
    master_id = create_page("Notion Master Map", parent_type="page",
                            parent_id=master_parent, icon="🗺️")
    if not master_id:
        print("FATAL: Could not create master map page")
        return
    print()

    # Step 4: Add content to master map page
    print("=" * 60)
    print("STEP 4: Add content to Master Map")
    print("=" * 60)
    append_blocks(master_id, master_content())
    print()

    # Step 5: Verify
    print("=" * 60)
    print("STEP 5: Verify")
    print("=" * 60)
    # Check Workspace children
    r = requests.get(f"{BASE}/blocks/{master_parent}/children?page_size=100", headers=HEADERS)
    if r.status_code == 200:
        blocks = r.json().get("results", [])
        print(f"  Workspace now has {len(blocks)} blocks")
        child_items = [b for b in blocks if b["type"] in ("child_page", "child_database")]
        for cp in child_items:
            t = cp["type"]
            title = cp.get(t, {}).get("title", "?")
            print(f"    {t}: {title}")
    else:
        print(f"  FAILED to verify Workspace: {r.status_code}")

    # Check Master Map content
    r = requests.get(f"{BASE}/blocks/{master_id}/children?page_size=100", headers=HEADERS)
    if r.status_code == 200:
        blocks = r.json().get("results", [])
        print(f"  Master Map has {len(blocks)} content blocks")
    else:
        print(f"  FAILED to verify Master Map: {r.status_code}")

    print(f"\nDone!")
    print(f"Workspace: https://www.notion.so/{master_parent.replace('-', '')}")
    print(f"Master Map: https://www.notion.so/{master_id.replace('-', '')}")


if __name__ == "__main__":
    run()
