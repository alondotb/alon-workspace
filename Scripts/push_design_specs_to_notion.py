#!/usr/bin/env python3
"""
Push VRT Design Specs to Notion
================================
Reads markdown spec files from ~/Desktop/Alon-Workspace/Docs/design-specs/
and creates them as child pages under the VRT Workspace page in Notion.

Usage:
    python3 push_design_specs_to_notion.py --token secret_xxx
"""

import json
import os
import re
import ssl
import sys
import time
import argparse
import certifi
from urllib.request import Request, urlopen
from urllib.error import HTTPError

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

VRT_WORKSPACE_PAGE_ID = "30a5308b-6bc5-80ef-ae57-e27dbfdfd1f2"
NOTION_VERSION = "2022-06-28"
RATE_LIMIT_DELAY = 0.35
SPECS_DIR = os.path.expanduser("~/Desktop/Alon-Workspace/Docs/design-specs")

SPEC_FILES = [
    ("00-overview.md", "Design Specs: Overview"),
    ("01-auth-onboarding.md", "Design Specs: Auth & Onboarding"),
    ("02-learning-core.md", "Design Specs: Learning Core"),
    ("03-projects.md", "Design Specs: Projects"),
    ("04-gamification.md", "Design Specs: Gamification"),
    ("05-social.md", "Design Specs: Social"),
    ("06-bug-hunt.md", "Design Specs: Bug Hunt"),
    ("07-parent-dashboard.md", "Design Specs: Parent Dashboard"),
    ("08-payments-trial.md", "Design Specs: Payments & Trial"),
    ("09-marketing-pages.md", "Design Specs: Marketing Pages"),
    ("10-emails.md", "Design Specs: Email Templates"),
    ("11-navigation-components.md", "Design Specs: Navigation & Components"),
]


def notion_request(method, endpoint, token, body=None):
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"  ERROR {e.code}: {error_body[:300]}")
        raise


def md_to_notion_blocks(md_content):
    """Convert markdown to Notion blocks. Handles headings, paragraphs, lists, and code blocks."""
    blocks = []
    lines = md_content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_text = "\n".join(code_lines)
            if code_text:
                # Notion code blocks have 2000 char limit per rich_text element
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": code_text[:2000]}}],
                        "language": lang if lang in ("python", "javascript", "html", "css", "json", "bash", "plain text") else "plain text",
                    }
                })
            i += 1
            continue

        # Heading 1
        if line.startswith("# "):
            text = line[2:].strip()
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })
            i += 1
            continue

        # Heading 2
        if line.startswith("## "):
            text = line[3:].strip()
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })
            i += 1
            continue

        # Heading 3
        if line.startswith("### "):
            text = line[4:].strip()
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })
            i += 1
            continue

        # Bulleted list item
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            text = re.sub(r"^\s*[-*]\s+", "", line).strip()
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })
            i += 1
            continue

        # Numbered list item
        if re.match(r"^\s*\d+\.\s+", line):
            text = re.sub(r"^\s*\d+\.\s+", "", line).strip()
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })
            i += 1
            continue

        # Horizontal rule
        if line.strip() in ("---", "***", "___"):
            blocks.append({"object": "block", "type": "divider", "divider": {}})
            i += 1
            continue

        # Table rows — convert to paragraphs (Notion table API is complex)
        if line.strip().startswith("|"):
            # Skip separator rows like |---|---|
            if re.match(r"^\s*\|[\s\-:|]+\|\s*$", line):
                i += 1
                continue
            text = line.strip()
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })
            i += 1
            continue

        # Blockquote
        if line.strip().startswith("> "):
            text = line.strip()[2:].strip()
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })
            i += 1
            continue

        # Regular paragraph (skip empty lines)
        text = line.strip()
        if text:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
            })

        i += 1

    return blocks


def create_page_with_content(token, parent_page_id, title, blocks):
    """Create a Notion page with content blocks. Notion limits 100 blocks per request."""
    # Create the page with first 100 blocks
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": [{"type": "text", "text": {"content": title}}]
        },
        "children": blocks[:100],
    }
    result = notion_request("POST", "pages", token, body)
    page_id = result["id"]

    # Append remaining blocks in batches of 100
    remaining = blocks[100:]
    while remaining:
        batch = remaining[:100]
        remaining = remaining[100:]
        time.sleep(RATE_LIMIT_DELAY)
        notion_request("PATCH", f"blocks/{page_id}/children", token, {"children": batch})

    return page_id


def main():
    parser = argparse.ArgumentParser(description="Push VRT Design Specs to Notion")
    parser.add_argument("--token", help="Notion API token")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating")
    args = parser.parse_args()

    token = args.token or os.environ.get("NOTION_API_KEY")
    if not token and not args.dry_run:
        print("ERROR: No Notion API token. Use --token or set NOTION_API_KEY")
        sys.exit(1)

    # Check which spec files exist
    existing = []
    missing = []
    for filename, title in SPEC_FILES:
        path = os.path.join(SPECS_DIR, filename)
        if os.path.exists(path):
            existing.append((filename, title, path))
        else:
            missing.append(filename)

    print(f"Found {len(existing)}/{len(SPEC_FILES)} spec files")
    if missing:
        print(f"Missing: {', '.join(missing)}")

    if args.dry_run:
        for filename, title, path in existing:
            size = os.path.getsize(path)
            with open(path) as f:
                content = f.read()
            blocks = md_to_notion_blocks(content)
            print(f"  {filename} ({size:,} bytes) → {len(blocks)} Notion blocks → \"{title}\"")
        return

    # Step 1: Create parent page "Design Specs"
    print("\nCreating 'Design Specs' parent page...")
    parent_body = {
        "parent": {"type": "page_id", "page_id": VRT_WORKSPACE_PAGE_ID},
        "properties": {
            "title": [{"type": "text", "text": {"content": "Design Specs"}}]
        },
        "children": [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": f"Screen-by-screen UI/UX design specs for the VRT MVP. {len(existing)} spec documents covering ~74 screens across all user flows."}}],
                    "icon": {"type": "emoji", "emoji": "🎨"},
                }
            }
        ],
    }
    result = notion_request("POST", "pages", token, parent_body)
    specs_parent_id = result["id"]
    print(f"  Created: {specs_parent_id}")
    time.sleep(RATE_LIMIT_DELAY)

    # Step 2: Create child pages for each spec
    print(f"\nCreating {len(existing)} spec pages...")
    success = 0
    for i, (filename, title, path) in enumerate(existing):
        try:
            with open(path) as f:
                content = f.read()
            blocks = md_to_notion_blocks(content)
            page_id = create_page_with_content(token, specs_parent_id, title, blocks)
            success += 1
            print(f"  [{i+1}/{len(existing)}] {title} ({len(blocks)} blocks)")
            time.sleep(RATE_LIMIT_DELAY)
        except Exception as e:
            print(f"  [{i+1}/{len(existing)}] FAILED: {title} — {e}")

    print(f"\nDone! {success}/{len(existing)} pages created")
    print(f"Parent page: https://notion.so/{specs_parent_id.replace('-', '')}")


if __name__ == "__main__":
    main()
