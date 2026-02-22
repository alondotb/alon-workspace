"""
Rewrite Notion Workspace pages with updated content reflecting Claude Code integration.
"""

import requests
import sys
import time
import os

API_KEY = os.environ.get("NOTION_API_KEY", "")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
BASE = "https://api.notion.com/v1"

# --- Page IDs ---
WORKSPACE_PAGE = "9a0ef9f8-e383-4a28-8a12-ba27fc0697cf"
VRT_PAGE = "30a5308b-6bc5-80ef-ae57-e27dbfdfd1f2"

# --- Blocks to delete ---
WORKSPACE_DELETE = [
    "a012a118-55d7-4174-b746-c9348cdff7d1",
    "3240dbb5-5ff8-4aba-8fc3-12c676922120",
    "cc1fa623-2598-4a23-8e0b-cb061ed7e436",
    "db45dabb-5b47-455a-8d8d-641d32bcec67",
    "baae8d90-0129-475c-9e0a-d2ca3509e2c9",
    "2c02d780-8d6c-4461-ba7f-68a463f02af2",
    "4b6e33a7-a540-4aaa-a865-7f50b564425d",
    "b3ffbd75-a27d-446d-a235-172cf65dac35",
    "c2d7c928-5a0a-4869-9808-5288d6f653f0",
    "44cb3e50-0c25-456f-8113-66f3dfa6719f",
    "4889845a-b6c5-4d3c-a988-219752656128",
    "dd0690cf-7b7b-46b0-86b6-27fea8ce5f82",
    "96f56981-f066-45d0-a146-ae1d2c6417be",
    "8d6a883d-1d6e-4c5b-b494-94ba2d2d1f70",
    "37277840-486d-4ea8-beff-d9d09d146b8b",
    "12f75fc8-e41a-4b1e-8f44-33347889e668",
    "d34ae56a-3dfe-464d-bee6-0d98166bebf7",
    "d9dba667-c343-41f2-b977-6b7ddeffe20a",
    "665dba21-64fc-4e89-9b77-647ef379f794",
    "7f59baa2-cb38-4ca6-a548-a162b1ba88f6",
    "aeb7eaa2-f920-44ad-b7c2-9add99d85d8e",
    "ae687bbd-eb63-4478-aea4-31bf8bf53a12",
    "b17a8360-1628-48f6-91fe-e5e208191833",
    "b4bad598-b12c-4844-afd8-1322d17eb49c",
    "944e29eb-3495-4486-b8a5-fd1d58bccafa",
]

VRT_DELETE = [
    # Old template blocks
    "14a49084-6646-489f-b356-1afa61856859",
    "259cf78f-e1e7-4dd8-b185-c0b2070b08ee",
    "ff5f3476-2e5e-45af-90a3-89ec56007219",
    "74ca1487-e2fd-4ac5-93aa-ed5b786fdec4",
    "251c17bb-8553-4bbf-ba11-6f8159830ff0",
    "a4146a32-e159-4d45-8eff-c2353445a417",
    "21c24d14-75e7-4369-93f6-3358996b0e8e",
    "d362ad4e-780a-4af6-87c4-d10c48d9294e",
    "b7ad0da4-0e14-435d-8e62-e53d9d111f95",
    "c7342c56-c36a-494c-a244-d0f066fa0664",
    "473f443a-2270-4956-8a8e-e616d294a60a",
    "30a5308b-6bc5-8003-a37c-d06696d25bff",
    "30a5308b-6bc5-805f-b660-f2d576fc0264",
    "30a5308b-6bc5-8032-8f01-f9d549d477a8",
    "30a5308b-6bc5-80a1-a1cb-cb506be9c679",
    "30a5308b-6bc5-80c9-bd4c-f3ffc3122dc0",
    "30a5308b-6bc5-8069-97e8-d4eb23c0b67c",
    "30a5308b-6bc5-8079-bd98-fc03ae75ab2f",
    "30a5308b-6bc5-809b-af5e-daf2304d8e63",
    # Duplicate new content from first failed run
    "30a5308b-6bc5-813c-b171-dec8b63d0f8b",
    "30a5308b-6bc5-8175-a762-d3e8bbe03bca",
    "30a5308b-6bc5-81b0-b0fe-e8fa08f4f88e",
    "30a5308b-6bc5-81ce-8bff-f0a95038f8b9",
    "30a5308b-6bc5-8112-9f44-c1be9ca9997e",
    "30a5308b-6bc5-8111-b558-c61c43439ec3",
    "30a5308b-6bc5-81a8-aff4-f1ecdbe9bf66",
    "30a5308b-6bc5-81bf-9eac-ebbad08ba7f5",
    "30a5308b-6bc5-8192-9a39-fc95e9da6f7c",
    "30a5308b-6bc5-813b-acad-d588615686d9",
    "30a5308b-6bc5-818c-9726-d99d595a1fa8",
    "30a5308b-6bc5-81e9-b400-f728a2dcda06",
    "30a5308b-6bc5-81e4-b9a7-c9f590965f3a",
    "30a5308b-6bc5-8123-9237-d816e4577186",
    "30a5308b-6bc5-8119-8f37-ce3bf4704436",
    "30a5308b-6bc5-81e4-b4e0-d03d731198c9",
    "30a5308b-6bc5-8121-aa91-d65354451a53",
    "30a5308b-6bc5-8126-a14f-c334a13b4c7d",
    "30a5308b-6bc5-81ed-80b7-c3ace5456ddc",
    "30a5308b-6bc5-81c4-b483-e09dfa2417ec",
    "30a5308b-6bc5-81b3-867e-d06001cdf635",
    "30a5308b-6bc5-8179-84ef-eb986c685010",
    "30a5308b-6bc5-813f-92a5-ef93742bfef4",
    "30a5308b-6bc5-81d4-9530-f5aeb7550dce",
    "30a5308b-6bc5-8121-bdb0-ed1e53434bf9",
    "30a5308b-6bc5-81ea-acc6-ea51e0bc63cb",
    "30a5308b-6bc5-8128-836b-f9c8313e1ebd",
    "30a5308b-6bc5-81ac-a66b-e149136cce5f",
    "30a5308b-6bc5-8184-940a-e76d8234e685",
    "30a5308b-6bc5-815f-aa86-d2451392658c",
    "30a5308b-6bc5-8104-8eed-e03caded4a3a",
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def rich_text(content, bold=False, italic=False, code=False):
    """Create a rich_text element."""
    annot = {}
    if bold: annot["bold"] = True
    if italic: annot["italic"] = True
    if code: annot["code"] = True
    obj = {"type": "text", "text": {"content": content}}
    if annot:
        obj["annotations"] = annot
    return obj


def heading(level, text):
    return {
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {"rich_text": [rich_text(text)]},
    }


def paragraph(*parts):
    """parts: rich_text dicts, a single string, or a list of rich_text dicts."""
    if len(parts) == 1 and isinstance(parts[0], str):
        rt = [rich_text(parts[0])]
    elif len(parts) == 1 and isinstance(parts[0], list):
        rt = parts[0]
    elif len(parts) == 1 and isinstance(parts[0], dict):
        rt = [parts[0]]
    else:
        rt = list(parts)
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rt},
    }


def bulleted(text_or_parts):
    if isinstance(text_or_parts, str):
        rt = [rich_text(text_or_parts)]
    else:
        rt = list(text_or_parts)
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rt},
    }


def numbered(text_or_parts):
    if isinstance(text_or_parts, str):
        rt = [rich_text(text_or_parts)]
    else:
        rt = list(text_or_parts)
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": rt},
    }


def callout(text, emoji="💡"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [rich_text(text)],
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


def divider():
    return {"object": "block", "type": "divider", "divider": {}}


def code_block(language, content):
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [rich_text(content)],
            "language": language,
        },
    }


def empty_paragraph():
    return paragraph("")


# ── API calls ────────────────────────────────────────────────────────────────

def delete_block(block_id):
    r = requests.delete(f"{BASE}/blocks/{block_id}", headers=HEADERS)
    if r.status_code == 200:
        print(f"  Deleted {block_id}")
    else:
        print(f"  FAILED to delete {block_id}: {r.status_code} {r.text[:120]}")
    return r.status_code == 200


def append_children(page_id, children):
    """Append blocks in batches of 100 (API limit)."""
    for i in range(0, len(children), 100):
        batch = children[i:i+100]
        r = requests.patch(
            f"{BASE}/blocks/{page_id}/children",
            headers=HEADERS,
            json={"children": batch},
        )
        if r.status_code == 200:
            print(f"  Appended {len(batch)} blocks (batch {i//100 + 1})")
        else:
            print(f"  FAILED to append batch {i//100 + 1}: {r.status_code} {r.text[:200]}")
            return False
    return True


# ── Content: Workspace (parent) ──────────────────────────────────────────────

def workspace_blocks():
    return [
        heading(1, "Your Workspace Hub"),
        callout(
            "This is your central workspace. One place for tools, workflows, and how Claude Code ties it all together.",
            "🏠"
        ),
        empty_paragraph(),

        # How it works
        heading(2, "How it works"),
        paragraph("Three pieces, one system:"),
        bulleted([
            rich_text("Notion", bold=True),
            rich_text(" = your system of record. Tools, plans, decisions, project tracking — it all lives here."),
        ]),
        bulleted([
            rich_text("Claude Code", bold=True),
            rich_text(" = your terminal assistant. Runs in your codebase, edits files, talks to Notion via API."),
        ]),
        bulleted([
            rich_text("The bridge", bold=True),
            rich_text(" = "),
            rich_text("tools.json", code=True),
            rich_text(" — a local snapshot of your tool stack that Claude reads on session start and syncs from this page."),
        ]),
        empty_paragraph(),
        divider(),

        # Tool Inventory
        heading(2, "Tool Inventory"),
        paragraph("Your full stack — every tool, what it does, and how it fits into the workflow. Managed in the database below."),
        # DB block 3408692e is kept in place
        empty_paragraph(),
        divider(),

        # Workflow
        heading(2, "Your workflow"),
        paragraph("Everything you do follows five steps:"),
        numbered([
            rich_text("Capture", bold=True),
            rich_text(" — Ideas, tasks, and requests go into Notion. Don't let anything live only in your head or Slack."),
        ]),
        numbered([
            rich_text("Plan", bold=True),
            rich_text(" — Weekly review: prioritize tasks, set goals, decide what gets built this week."),
        ]),
        numbered([
            rich_text("Produce", bold=True),
            rich_text(" — Build it. Matan codes, you handle content/design, Claude Code assists both."),
        ]),
        numbered([
            rich_text("Publish", bold=True),
            rich_text(" — Ship to site, YouTube, socials. Log every published link back in Notion."),
        ]),
        numbered([
            rich_text("Measure", bold=True),
            rich_text(" — Check views, leads, sales. Capture learnings and feed them back into Capture."),
        ]),
        empty_paragraph(),
        divider(),

        # Claude Code integration
        heading(2, "Claude Code integration"),
        paragraph("What Claude Code actually does for you:"),
        bulleted("Reads and writes Notion pages via API — no copy-pasting between tools."),
        bulleted([
            rich_text("Syncs "),
            rich_text("tools.json", code=True),
            rich_text(" on session start so it always knows your current stack."),
        ]),
        bulleted("Runs scripts, builds tools, manages code — all from the terminal."),
        bulleted([
            rich_text("Has workspace instructions ("),
            rich_text("CLAUDE.md", code=True),
            rich_text(") that auto-load when you "),
            rich_text("cd", code=True),
            rich_text(" into the workspace."),
        ]),
        bulleted("Can be given memory across sessions — it remembers what you tell it to."),
        bulleted([
            rich_text("Works in terminal "),
            rich_text("or", italic=True),
            rich_text(" inside VS Code via the extension ("),
            rich_text("Anthropic.claude-code", code=True),
            rich_text(")."),
        ]),
        empty_paragraph(),
        divider(),

        # Quick start
        heading(2, "Quick start"),
        paragraph(
            rich_text("Option A — Terminal:", bold=True),
        ),
        numbered("Open your terminal."),
        numbered([
            rich_text("Run "),
            rich_text("claude", code=True),
            rich_text(" to start a session."),
        ]),
        numbered([
            rich_text("Navigate to your workspace: "),
            rich_text("cd ~/Desktop/Alon-Workspace", code=True),
        ]),
        empty_paragraph(),
        paragraph(
            rich_text("Option B — VS Code:", bold=True),
        ),
        numbered([
            rich_text("Install the extension: "),
            rich_text("Anthropic.claude-code", code=True),
        ]),
        numbered("Open your workspace folder in VS Code."),
        numbered("Claude is right there in the editor — same capabilities, visual interface."),
        empty_paragraph(),
        paragraph("Either way, Claude auto-syncs with Notion and knows your tools, workflow, and projects."),
        empty_paragraph(),
        divider(),

        # Principles
        heading(2, "Principles"),
        bulleted([
            rich_text("One source of truth.", bold=True),
            rich_text(" Everything lives in Notion or Git. No stray docs, no lost notes."),
        ]),
        bulleted([
            rich_text("Automate the boring stuff.", bold=True),
            rich_text(" If you're doing it more than twice, script it."),
        ]),
        bulleted([
            rich_text("Keep it simple.", bold=True),
            rich_text(" Don't over-engineer. Build what you need now, improve later."),
        ]),
        bulleted([
            rich_text("Claude Code handles the technical glue.", bold=True),
            rich_text(" Syncing, scripting, API calls, file management — let Claude do the wiring."),
        ]),
        empty_paragraph(),
        divider(),

        # tools.json reference
        heading(2, "tools.json"),
        paragraph([
            rich_text("This is the local file Claude reads on startup. It's synced from the Tool Inventory database above. Location: "),
            rich_text("~/Desktop/Alon-Workspace/tools.json", code=True),
        ]),
        code_block("json", '[\n  {\n    "name": "Notion",\n    "category": "System of Record",\n    "role": "Plans, docs, databases, project tracking"\n  },\n  {\n    "name": "Claude Code",\n    "category": "AI Assistant",\n    "role": "Terminal assistant — code, scripts, Notion sync"\n  },\n  {\n    "name": "VS Code",\n    "category": "Editor",\n    "role": "Code editing, Claude Code extension"\n  },\n  {\n    "name": "GitHub",\n    "category": "Version Control",\n    "role": "Code hosting, collaboration"\n  }\n]'),
        empty_paragraph(),

        # Replacement DB kept (2ed05f69) — in place
    ]


# ── Content: VRT (child) ────────────────────────────────────────────────────

def vrt_blocks():
    return [
        heading(1, "VRT Workspace"),
        callout(
            "VRT (Virtual Techies) — self-paced coding education for kids aged 10-14. "
            "Kids learn real programming through a 2D campaign with video-based quests. No teacher needed. "
            "This page is the VRT-specific workspace.",
            "🎮"
        ),
        empty_paragraph(),

        # The team
        heading(2, "The team"),
        bulleted([
            rich_text("Alon", bold=True),
            rich_text(" — product, design, business"),
        ]),
        bulleted([
            rich_text("Matan", bold=True),
            rich_text(" — R&D, development"),
        ]),
        empty_paragraph(),
        divider(),

        # What Claude Code does for VRT
        heading(2, "What Claude Code does for VRT"),
        bulleted("Builds tools and scripts (file viewer, automation scripts, utilities)."),
        bulleted("Manages the codebase and GitHub repos."),
        bulleted("Syncs with Notion for project tracking and documentation."),
        bulleted("Helps Alon learn programming along the way."),
        empty_paragraph(),
        divider(),

        # VRT workflow
        heading(2, "VRT workflow"),
        numbered([
            rich_text("Capture", bold=True),
            rich_text(" — Ideas and tasks go into Notion Tasks. Feature requests, bugs, content ideas — all captured here."),
        ]),
        numbered([
            rich_text("Plan", bold=True),
            rich_text(" — Weekly review in Slack, then prioritize in Notion. Decide what Matan builds and what Alon produces."),
        ]),
        numbered([
            rich_text("Produce", bold=True),
            rich_text(" — Matan codes, Alon produces content and design. Claude Code assists both — scripting, file management, code help."),
        ]),
        numbered([
            rich_text("Publish", bold=True),
            rich_text(" — Push to site, YouTube, socials. Log every published link back in Notion."),
        ]),
        numbered([
            rich_text("Measure", bold=True),
            rich_text(" — Check views, leads, sales. Capture learnings and feed them back into the next cycle."),
        ]),
        empty_paragraph(),
        divider(),

        # Key local paths
        heading(2, "Key local paths"),
        bulleted([
            rich_text("~/Desktop/Alon-Workspace/", code=True),
            rich_text(" — workspace hub (tools, scripts, config)"),
        ]),
        bulleted([
            rich_text("~/Downloads/virtual-techies-master/", code=True),
            rich_text(" — source materials (course content, syllabus, financials, contracts)"),
        ]),
        bulleted([
            rich_text("~/Desktop/Alon-Workspace/Scripts/", code=True),
            rich_text(" — automation tools and utility scripts"),
        ]),
        empty_paragraph(),
        divider(),

        # VRT Tool Inventory
        heading(2, "VRT Tool Inventory"),
        paragraph("VRT-specific tools and services tracked in the databases below."),
        # DB blocks 1c4410eb and 9a174461 are kept in place
    ]


# ── Main ─────────────────────────────────────────────────────────────────────

def run():
    print("=" * 60)
    print("STEP 1: Delete old blocks from Workspace page")
    print("=" * 60)
    ws_ok = 0
    for bid in WORKSPACE_DELETE:
        if delete_block(bid):
            ws_ok += 1
        time.sleep(0.35)  # rate limit safety
    print(f"\n  Workspace: {ws_ok}/{len(WORKSPACE_DELETE)} deleted\n")

    print("=" * 60)
    print("STEP 2: Delete old blocks from VRT page")
    print("=" * 60)
    vrt_ok = 0
    for bid in VRT_DELETE:
        if delete_block(bid):
            vrt_ok += 1
        time.sleep(0.35)
    print(f"\n  VRT: {vrt_ok}/{len(VRT_DELETE)} deleted\n")

    print("=" * 60)
    print("STEP 3: Append new content to Workspace page")
    print("=" * 60)
    ws_append = append_children(WORKSPACE_PAGE, workspace_blocks())
    print(f"  Workspace append: {'OK' if ws_append else 'FAILED'}\n")

    print("=" * 60)
    print("STEP 4: Append new content to VRT page")
    print("=" * 60)
    vrt_append = append_children(VRT_PAGE, vrt_blocks())
    print(f"  VRT append: {'OK' if vrt_append else 'FAILED'}\n")

    # Verification
    print("=" * 60)
    print("STEP 5: Verify pages")
    print("=" * 60)
    for name, pid in [("Workspace", WORKSPACE_PAGE), ("VRT", VRT_PAGE)]:
        r = requests.get(f"{BASE}/blocks/{pid}/children?page_size=50", headers=HEADERS)
        if r.status_code == 200:
            blocks = r.json().get("results", [])
            types = [b["type"] for b in blocks]
            print(f"  {name}: {len(blocks)} blocks — types: {types[:10]}...")
        else:
            print(f"  {name}: FAILED to fetch — {r.status_code}")

    print("\nDone!")


if __name__ == "__main__":
    run()
