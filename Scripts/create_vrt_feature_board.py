#!/usr/bin/env python3
"""
Create VRT Feature Board in Notion
===================================
Creates a database under the VRT Workspace page and populates it with
~87 tasks from the MVP summary (dependency-aware task breakdown).

Usage:
    export NOTION_API_KEY="secret_xxx"
    python3 create_vrt_feature_board.py

Or:
    python3 create_vrt_feature_board.py --token secret_xxx

Setup:
    1. Create a Notion integration at https://www.notion.so/my-integrations
    2. Share the "Workspace - VRT" page with that integration
    3. Run this script with the token
"""

import json
import os
import ssl
import sys
import time
import argparse
import certifi
from urllib.request import Request, urlopen
from urllib.error import HTTPError

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

# ── Config ──────────────────────────────────────────────────────────────────

VRT_WORKSPACE_PAGE_ID = "30a5308b-6bc5-80ef-ae57-e27dbfdfd1f2"
NOTION_VERSION = "2022-06-28"
RATE_LIMIT_DELAY = 0.35  # seconds between API calls


# ── Notion API helpers ──────────────────────────────────────────────────────

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
        print(f"  ERROR {e.code}: {error_body}")
        raise


def create_database(token):
    """Create the VRT Feature Board database with full schema."""
    body = {
        "parent": {"type": "page_id", "page_id": VRT_WORKSPACE_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "VRT Feature Board"}}],
        "is_inline": True,
        "properties": {
            "Name": {"title": {}},
            "Task ID": {"rich_text": {}},
            "Department": {
                "select": {
                    "options": [
                        {"name": "Product", "color": "purple"},
                        {"name": "R&D", "color": "blue"},
                        {"name": "Design", "color": "pink"},
                        {"name": "Marketing", "color": "orange"},
                        {"name": "Support", "color": "green"},
                    ]
                }
            },
            "Owner": {
                "select": {
                    "options": [
                        {"name": "Alon", "color": "purple"},
                        {"name": "Matan", "color": "blue"},
                        {"name": "Unassigned", "color": "gray"},
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Backlog", "color": "default"},
                        {"name": "To Do", "color": "yellow"},
                        {"name": "In Progress", "color": "blue"},
                        {"name": "Done", "color": "green"},
                    ]
                }
            },
            "Priority": {
                "select": {
                    "options": [
                        {"name": "P0-Critical", "color": "red"},
                        {"name": "P1-High", "color": "orange"},
                        {"name": "P2-Medium", "color": "yellow"},
                        {"name": "P3-Low", "color": "default"},
                    ]
                }
            },
            "Phase": {
                "select": {
                    "options": [
                        {"name": "1-Foundation", "color": "red"},
                        {"name": "2-Core", "color": "orange"},
                        {"name": "3-Content", "color": "yellow"},
                        {"name": "4-Polish", "color": "green"},
                        {"name": "5-Launch", "color": "blue"},
                    ]
                }
            },
            "Blocks": {"rich_text": {}},
            "Blocked By": {"rich_text": {}},
            "Done When": {"rich_text": {}},
            "Category": {
                "select": {
                    "options": [
                        {"name": "Auth", "color": "red"},
                        {"name": "Payments", "color": "orange"},
                        {"name": "Lessons", "color": "yellow"},
                        {"name": "Questions", "color": "green"},
                        {"name": "Gamification", "color": "blue"},
                        {"name": "Avatar", "color": "purple"},
                        {"name": "Social", "color": "pink"},
                        {"name": "Content", "color": "brown"},
                        {"name": "Infrastructure", "color": "gray"},
                        {"name": "Design-System", "color": "default"},
                        {"name": "UI-UX", "color": "yellow"},
                        {"name": "Art", "color": "pink"},
                        {"name": "Marketing", "color": "orange"},
                        {"name": "Support", "color": "green"},
                        {"name": "Legal", "color": "red"},
                    ]
                }
            },
        },
    }
    print("Creating database 'VRT Feature Board'...")
    result = notion_request("POST", "databases", token, body)
    db_id = result["id"]
    print(f"  Database created: {db_id}")
    return db_id


def add_task(token, db_id, task):
    """Add a single task to the database."""
    properties = {
        "Name": {"title": [{"text": {"content": task["name"]}}]},
        "Task ID": {"rich_text": [{"text": {"content": task["id"]}}]},
        "Department": {"select": {"name": task["department"]}},
        "Owner": {"select": {"name": task["owner"]}},
        "Status": {"select": {"name": task["status"]}},
        "Priority": {"select": {"name": task["priority"]}},
        "Phase": {"select": {"name": task["phase"]}},
        "Category": {"select": {"name": task["category"]}},
    }
    if task.get("blocks"):
        properties["Blocks"] = {"rich_text": [{"text": {"content": task["blocks"]}}]}
    if task.get("blocked_by"):
        properties["Blocked By"] = {"rich_text": [{"text": {"content": task["blocked_by"]}}]}
    if task.get("done_when"):
        # Notion rich_text content max is 2000 chars
        done_text = task["done_when"][:2000]
        properties["Done When"] = {"rich_text": [{"text": {"content": done_text}}]}

    body = {"parent": {"database_id": db_id}, "properties": properties}
    notion_request("POST", "pages", token, body)


# ── Task Data ───────────────────────────────────────────────────────────────
# All 87 tasks from summary.md with derived Phase, Priority, and Category

TASKS = [
    # ═══ PRODUCT (P1-P14) ═══
    {
        "id": "P1", "name": "Define MVP feature scope",
        "department": "Product", "owner": "Alon", "status": "Done",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Infrastructure",
        "blocks": "All departments", "blocked_by": "",
        "done_when": "Final feature list signed off. What's in, what's out."
    },
    {
        "id": "P2", "name": "Define pricing & subscription tiers",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Payments",
        "blocks": "R3, M4", "blocked_by": "P1",
        "done_when": "Exact NIS amounts for Basic/Premium monthly/yearly, free trial terms (7 days, 5 lessons), credit card requirements"
    },
    {
        "id": "P3", "name": "Define lesson curriculum & order",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Lessons",
        "blocks": "R16, D5", "blocked_by": "P1",
        "done_when": "All 28 lesson topics listed in teaching order, prerequisites mapped"
    },
    {
        "id": "P4", "name": "Define gamification rules",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "1-Foundation", "category": "Gamification",
        "blocks": "R8, R9, R10", "blocked_by": "P1",
        "done_when": "XP values per action, coin earn/spend rates, level thresholds (1-30), streak multipliers, hint costs (5/15/30 coins)"
    },
    {
        "id": "P5", "name": "Define achievement list",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "Gamification",
        "blocks": "R13, D13", "blocked_by": "P4",
        "done_when": "All 30-40 achievements specified: name, description, unlock condition, coin reward, rarity"
    },
    {
        "id": "P6", "name": "Define question difficulty calibration",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "1-Foundation", "category": "Questions",
        "blocks": "R7, R16", "blocked_by": "P3",
        "done_when": "Rules for Easy/Medium/Hard/Challenge per lesson, min-to-advance per lesson (5-8), question type distribution"
    },
    {
        "id": "P7", "name": "Define Bug Hunt game rules",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "Gamification",
        "blocks": "R14, D14", "blocked_by": "P4",
        "done_when": "3 modes fully specced: Quick Play (5 bugs, timing), Endless (difficulty curve), Daily Challenge (selection criteria, leaderboard rules)"
    },
    {
        "id": "P8", "name": "Define onboarding flow",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Auth",
        "blocks": "R2, D4", "blocked_by": "P1",
        "done_when": "Step-by-step first-time experience: parent signup -> add child -> child logs in -> avatar selection -> first lesson. Every screen defined."
    },
    {
        "id": "P9", "name": "Define parent dashboard spec",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R12, D12", "blocked_by": "P1",
        "done_when": "What data parents see: lessons completed, time spent, question stats, project progress, achievements. Weekly email content. Time limit rules."
    },
    {
        "id": "P10", "name": "Define beta program",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "4-Polish", "category": "Marketing",
        "blocks": "M9, R22", "blocked_by": "P1, M1",
        "done_when": "Beta size (30-50 families), recruitment criteria, duration, feedback mechanisms, success criteria"
    },
    {
        "id": "P11", "name": "Define content QA process",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Content",
        "blocks": "R16, R17, R18", "blocked_by": "P6",
        "done_when": "How questions are reviewed before going live: who tests, how code execution is verified, how difficulty is validated"
    },
    {
        "id": "P12", "name": "Define success metrics",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Infrastructure",
        "blocks": "M12, R21", "blocked_by": "P1",
        "done_when": "Exact KPIs with targets: trial->paid >15%, Day-7 retention >40%, lesson 10 completion >60%, churn <8%"
    },
    {
        "id": "P13", "name": "Legal: Terms of Service & Privacy Policy",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "4-Polish", "category": "Legal",
        "blocks": "R23, M4", "blocked_by": "P1",
        "done_when": "Hebrew ToS and privacy policy written, reviewed, covering kids' data (COPPA-like), published on site"
    },
    {
        "id": "P14", "name": "Define email sequences",
        "department": "Product", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "Content",
        "blocks": "R12, D16", "blocked_by": "P9",
        "done_when": "All automated emails specced: welcome, trial day 3 nudge, trial ending (day 6), payment failed, weekly parent report, win-back (churned user)"
    },

    # ═══ R&D PLATFORM (R1-R26) ═══
    {
        "id": "R1", "name": "Project setup",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Infrastructure",
        "blocks": "All R&D tasks", "blocked_by": "",
        "done_when": "Repo, CI/CD, Next.js + Tailwind + Prisma + PostgreSQL deployed to staging"
    },
    {
        "id": "R2", "name": "Auth system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "2-Core", "category": "Auth",
        "blocks": "R3, R5, R12", "blocked_by": "R1, P8, D4",
        "done_when": "Parent signup (email + Google), child account creation, email verification, password reset, parent/child relationship"
    },
    {
        "id": "R3", "name": "Stripe subscription integration",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "2-Core", "category": "Payments",
        "blocks": "R22", "blocked_by": "R2, P2",
        "done_when": "Checkout flow for 4 plans (basic/premium x monthly/yearly), webhooks, customer portal, plan upgrade/downgrade, cancellation"
    },
    {
        "id": "R4", "name": "Free trial system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "Payments",
        "blocks": "R22", "blocked_by": "R3, P2",
        "done_when": "7-day trial, 5-lesson limit, no credit card required, trial->paid conversion flow, trial expiry UX"
    },
    {
        "id": "R5", "name": "Lesson viewer with interactive code blocks",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "2-Core", "category": "Lessons",
        "blocks": "R7", "blocked_by": "R1, R6, D5",
        "done_when": "Lesson page renders written content with inline runnable/editable/resettable code blocks (Monaco Editor). Run -> output. Reset -> original code."
    },
    {
        "id": "R6", "name": "Code execution service",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "2-Core", "category": "Infrastructure",
        "blocks": "R5, R7, R14", "blocked_by": "R1",
        "done_when": "Sandboxed Python execution (Docker/Piston), 5s timeout, 50MB memory, no network, rate limited (10/min/user), kid-friendly error messages"
    },
    {
        "id": "R7", "name": "Question system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "2-Core", "category": "Questions",
        "blocks": "R10", "blocked_by": "R5, R6, P6, D7",
        "done_when": "5 question types (code_write, code_fix, multiple_choice, output_predict, fill_blank), auto-grading, progressive difficulty, min-to-advance gating, 3-tier hints (coin cost)"
    },
    {
        "id": "R8", "name": "XP & leveling system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "Gamification",
        "blocks": "R9", "blocked_by": "R1, P4, D9",
        "done_when": "XP earned per action, level calculation (1-30), level titles displayed, level-up celebration trigger"
    },
    {
        "id": "R9", "name": "TechCoins economy",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "Gamification",
        "blocks": "R5, R11", "blocked_by": "R8, P4",
        "done_when": "Coins earned (questions, projects, streaks, logins, achievements), coins spent (avatar items, hints), balance display, transaction log"
    },
    {
        "id": "R10", "name": "Encouragement engine",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Gamification",
        "blocks": "", "blocked_by": "R7, P4, D8",
        "done_when": "Confetti on correct answers, streak tracking + multiplier display, difficulty tier completion celebrations, 'Come Back Later' flow, daily login encouragement"
    },
    {
        "id": "R11", "name": "Avatar system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "3-Content", "category": "Avatar",
        "blocks": "R15", "blocked_by": "R9, D2, D3",
        "done_when": "8-10 character selection, outfit/item inventory, equip/unequip, TechCoin purchasing, avatar displayed on profile + leaderboard"
    },
    {
        "id": "R12", "name": "Parent dashboard + automated emails",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "3-Content", "category": "UI-UX",
        "blocks": "", "blocked_by": "R2, P9, P14, D12, D16",
        "done_when": "Parent sees child progress (lessons, questions, time, projects, achievements). Weekly email auto-sent. Daily time limit enforcement."
    },
    {
        "id": "R13", "name": "Achievement system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Gamification",
        "blocks": "", "blocked_by": "R7, R8, R9, P5, D13",
        "done_when": "30-40 achievements, unlock condition triggers, celebration animation trigger, coin reward on unlock, displayed on profile"
    },
    {
        "id": "R14", "name": "Bug Hunt mini-game",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Gamification",
        "blocks": "", "blocked_by": "R6, R7, R9, P7, D14",
        "done_when": "Quick Play (5 bugs, timed), Endless Mode (increasing difficulty), Daily Challenge (shared leaderboard). Draws from mini-game question bank. Rewards TechCoins + XP."
    },
    {
        "id": "R15", "name": "Profile page",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Social",
        "blocks": "R16", "blocked_by": "R11, R13, D11",
        "done_when": "Public profile: avatar, level, XP, badges, current lesson, join date, 'about me' text"
    },
    {
        "id": "R16", "name": "Friend system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P3-Low", "phase": "4-Polish", "category": "Social",
        "blocks": "R17", "blocked_by": "R15, D11",
        "done_when": "Send/accept friend requests, friends list, see friends' profiles + online status"
    },
    {
        "id": "R17", "name": "Leaderboard",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P3-Low", "phase": "4-Polish", "category": "Social",
        "blocks": "", "blocked_by": "R16, R14, D11",
        "done_when": "Global XP ranking, weekly ranking, friends ranking, Bug Hunt daily ranking"
    },
    {
        "id": "R18", "name": "Project system",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Lessons",
        "blocks": "", "blocked_by": "R6, P3, D10",
        "done_when": "7 guided multi-step projects, auto-graded final submission, certificate tracking (which projects completed)"
    },
    {
        "id": "R19", "name": "Video player (premium tier)",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Lessons",
        "blocks": "", "blocked_by": "R3, R5, D5",
        "done_when": "Self-hosted video embedded in lesson page, gated behind premium subscription check, progress tracking, no YouTube"
    },
    {
        "id": "R20", "name": "Landing page",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "4-Polish", "category": "Marketing",
        "blocks": "R4", "blocked_by": "R1, D17, M3, P13",
        "done_when": "Hero, product explanation, pricing, testimonials section, CTA to free trial, SEO meta tags"
    },
    {
        "id": "R21", "name": "Analytics setup",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "Infrastructure",
        "blocks": "", "blocked_by": "R1",
        "done_when": "PostHog/Mixpanel integrated, key events tracked (lesson start/complete, question attempt, purchase, login), Sentry error monitoring"
    },
    {
        "id": "R22", "name": "Beta deployment",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "5-Launch", "category": "Infrastructure",
        "blocks": "M10", "blocked_by": "R2-R19, P10",
        "done_when": "Staging -> production, monitoring, alerting, database backups, load testing, security audit (auth, code execution, XSS/CSRF)"
    },
    {
        "id": "R23", "name": "Legal pages",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Legal",
        "blocks": "R20", "blocked_by": "P13",
        "done_when": "Terms of Service + Privacy Policy pages on the site"
    },
    {
        "id": "R24", "name": "Admin panel / content tool",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "Infrastructure",
        "blocks": "R16", "blocked_by": "R1, R5, R7",
        "done_when": "Simple admin interface to manage lessons, questions, projects, view users, manage subscriptions. Makes content entry faster."
    },
    {
        "id": "R25", "name": "Daily login streak tracking",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P3-Low", "phase": "3-Content", "category": "Gamification",
        "blocks": "", "blocked_by": "R9, R13",
        "done_when": "Track consecutive login days, streak multiplier on coin rewards, streak-based achievements"
    },
    {
        "id": "R26", "name": "Blog / SEO pages",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P3-Low", "phase": "4-Polish", "category": "Marketing",
        "blocks": "", "blocked_by": "R1, D17",
        "done_when": "Blog section for marketing content, proper meta tags, sitemap, structured data"
    },

    # ═══ R&D CONTENT (R27-R34) ═══
    {
        "id": "R27", "name": "Write lessons 1-14",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "3-Content", "category": "Content",
        "blocks": "R29, R31", "blocked_by": "P3, R5, R24",
        "done_when": "14 written lessons in Hebrew with interactive code blocks, optimized for ages 10-14"
    },
    {
        "id": "R28", "name": "Write lessons 15-28",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "3-Content", "category": "Content",
        "blocks": "R30, R31", "blocked_by": "P3, R5, R24",
        "done_when": "Remaining 14 lessons (lesson 28 = Final Project brief)"
    },
    {
        "id": "R29", "name": "Record videos 1-14",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P1-High", "phase": "3-Content", "category": "Content",
        "blocks": "", "blocked_by": "R27, R19",
        "done_when": "14 screen recording + face cam videos in Hebrew (~5-15 min each), edited, uploaded to self-hosted storage"
    },
    {
        "id": "R30", "name": "Record videos 15-28",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Content",
        "blocks": "", "blocked_by": "R28, R19",
        "done_when": "Remaining ~14 videos (lesson 28 = brief intro only)"
    },
    {
        "id": "R31", "name": "Write lesson questions (550-600)",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P0-Critical", "phase": "3-Content", "category": "Questions",
        "blocks": "R22", "blocked_by": "R27, R28, P6, P11, R7",
        "done_when": "~20 questions per lesson, all 5 types, progressive difficulty, hints, test cases, explanations. All auto-grading correctly."
    },
    {
        "id": "R32", "name": "Write mini-game questions (200)",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Questions",
        "blocks": "R22", "blocked_by": "P7, R7",
        "done_when": "200 quick-fire questions for Bug Hunt, multiple choice / spot-the-error / output prediction"
    },
    {
        "id": "R33", "name": "Write 7 projects",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Content",
        "blocks": "R22", "blocked_by": "R18, P3",
        "done_when": "Guided steps, starter code, auto-grading test cases, acceptance criteria. In Hebrew, for ages 10-14."
    },
    {
        "id": "R34", "name": "Office hours setup",
        "department": "R&D", "owner": "Matan", "status": "Backlog",
        "priority": "P3-Low", "phase": "4-Polish", "category": "Support",
        "blocks": "", "blocked_by": "R12",
        "done_when": "Weekly Zoom/Meet link embedded in platform, email notifications to parents, recording upload flow"
    },

    # ═══ DESIGN (D1-D22) ═══
    {
        "id": "D1", "name": "Brand identity",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Design-System",
        "blocks": "D2, D3, D4, D5", "blocked_by": "P1",
        "done_when": "Logo, color palette, typography, style guide document delivered"
    },
    {
        "id": "D2", "name": "Avatar characters (8-10)",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "Art",
        "blocks": "D3, R11", "blocked_by": "D1",
        "done_when": "8-10 unique character illustrations in brand style"
    },
    {
        "id": "D3", "name": "Avatar items/outfits (15-20)",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "Art",
        "blocks": "R11", "blocked_by": "D2",
        "done_when": "15-20 purchasable cosmetic items matching avatar art style"
    },
    {
        "id": "D4", "name": "Design system / component library",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Design-System",
        "blocks": "D5, D7, D11, D12, D14", "blocked_by": "D1",
        "done_when": "Buttons, cards, inputs, forms, modals, tooltips, navigation -- all components spec'd and delivered"
    },
    {
        "id": "D5", "name": "Lesson viewer UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P0-Critical", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R5, R19", "blocked_by": "D1, D4, P3",
        "done_when": "Layout for: written content with interactive code blocks + Run/Reset buttons + output panel + video player (premium). Desktop + tablet."
    },
    {
        "id": "D6", "name": "Code editor theme",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R5", "blocked_by": "D1",
        "done_when": "Kid-friendly Monaco Editor theme: colors, font, cursor. Not intimidating."
    },
    {
        "id": "D7", "name": "Question UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R7", "blocked_by": "D4, P6",
        "done_when": "Layouts for all 5 types: code_write, code_fix, multiple_choice, output_predict, fill_blank. Difficulty tier indicators."
    },
    {
        "id": "D8", "name": "Celebration animations",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "Art",
        "blocks": "R10, R13", "blocked_by": "D1",
        "done_when": "Confetti burst, streak fire effect, level-up fanfare, difficulty tier completion, achievement unlock. Specs or Lottie files."
    },
    {
        "id": "D9", "name": "Progress indicators",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R8", "blocked_by": "D4",
        "done_when": "XP bar, level badge, lesson map/list with completion states, streak counter"
    },
    {
        "id": "D10", "name": "Project UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R18", "blocked_by": "D4",
        "done_when": "Guided step layout, progress indicator through steps, submission flow, completion celebration"
    },
    {
        "id": "D11", "name": "Profile, friends, leaderboard UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "UI-UX",
        "blocks": "R15, R16, R17", "blocked_by": "D4",
        "done_when": "Profile page layout, friend request flow, friends list, leaderboard table (global/weekly/friends/Bug Hunt)"
    },
    {
        "id": "D12", "name": "Parent dashboard UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R12", "blocked_by": "D4, P9",
        "done_when": "Clean, trustworthy dashboard: child progress charts, lesson completion, question stats, time spent, achievements. Time limit settings."
    },
    {
        "id": "D13", "name": "Achievement badges (30-40)",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "Art",
        "blocks": "R13", "blocked_by": "D1, P5",
        "done_when": "30-40 unique badge/icon illustrations for all achievement types"
    },
    {
        "id": "D14", "name": "Bug Hunt game UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "UI-UX",
        "blocks": "R14", "blocked_by": "D4, P7",
        "done_when": "Game screen for all 3 modes, bug reveal animation, timer, fix confirmation, score display, Daily Challenge leaderboard"
    },
    {
        "id": "D15", "name": "Hint UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "2-Core", "category": "UI-UX",
        "blocks": "R7", "blocked_by": "D4",
        "done_when": "Tiered hint reveal interface, coin cost display, 'buy hint' confirmation"
    },
    {
        "id": "D16", "name": "Email templates",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "3-Content", "category": "UI-UX",
        "blocks": "R12", "blocked_by": "D1, P14",
        "done_when": "Weekly parent report email, welcome email, trial ending email, payment failed email"
    },
    {
        "id": "D17", "name": "Landing page design",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "4-Polish", "category": "UI-UX",
        "blocks": "R20, M4", "blocked_by": "D1, P2",
        "done_when": "Hero section, feature showcase, pricing table (Basic vs Premium), testimonials area, CTA. Desktop + mobile."
    },
    {
        "id": "D18", "name": "Pricing page design",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "UI-UX",
        "blocks": "R20", "blocked_by": "D17, P2",
        "done_when": "Monthly vs yearly toggle, Basic vs Premium comparison, feature list, FAQ section"
    },
    {
        "id": "D19", "name": "Auth flow UI",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "2-Core", "category": "Auth",
        "blocks": "R2", "blocked_by": "D4, D2, P8",
        "done_when": "Parent signup, login, add child, child login, avatar selection (onboarding)"
    },
    {
        "id": "D20", "name": "404 / error / empty states",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P3-Low", "phase": "4-Polish", "category": "UI-UX",
        "blocks": "", "blocked_by": "D1, D2",
        "done_when": "Error pages, empty lesson list, no friends yet, no achievements yet -- all with character illustrations"
    },
    {
        "id": "D21", "name": "Marketing materials",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "5-Launch", "category": "Marketing",
        "blocks": "M5, M8", "blocked_by": "D1, D17",
        "done_when": "Social media templates, feature graphics, app screenshots, explainer graphics"
    },
    {
        "id": "D22", "name": "Blog design",
        "department": "Design", "owner": "Alon", "status": "Backlog",
        "priority": "P3-Low", "phase": "4-Polish", "category": "UI-UX",
        "blocks": "R26", "blocked_by": "D4",
        "done_when": "Blog list page, blog post template, responsive"
    },

    # ═══ MARKETING (M1-M17) ═══
    {
        "id": "M1", "name": "Market research",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P0-Critical", "phase": "1-Foundation", "category": "Marketing",
        "blocks": "M2, M3, P10", "blocked_by": "P1",
        "done_when": "10-20 Israeli parents of kids 10-14 interviewed. Pain points documented. Willingness to pay validated."
    },
    {
        "id": "M2", "name": "Competitive analysis",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "1-Foundation", "category": "Marketing",
        "blocks": "M3", "blocked_by": "M1",
        "done_when": "Every competitor reviewed (Codecademy, CodeCombat, Tynker, Scratch, etc.). Hebrew market gaps identified. Feature comparison matrix."
    },
    {
        "id": "M3", "name": "Positioning & messaging",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "1-Foundation", "category": "Marketing",
        "blocks": "M4, M5, M8", "blocked_by": "M1, M2, D1",
        "done_when": "Core messaging in Hebrew: tagline, value proposition, key differentiators, tone of voice. Parent-facing AND kid-facing messaging."
    },
    {
        "id": "M4", "name": "Landing page copy",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "4-Polish", "category": "Marketing",
        "blocks": "R20", "blocked_by": "M3, D17, P2",
        "done_when": "All landing page text written in Hebrew: hero, features, pricing, FAQ, CTA"
    },
    {
        "id": "M5", "name": "Social media setup",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Marketing",
        "blocks": "M6", "blocked_by": "D1, M3",
        "done_when": "Instagram, TikTok, YouTube, Facebook accounts created with brand assets. Content calendar planned."
    },
    {
        "id": "M6", "name": "'Building in public' series",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Marketing",
        "blocks": "M9", "blocked_by": "M5",
        "done_when": "Ongoing content: behind-the-scenes development, design previews, progress updates. Builds audience pre-launch."
    },
    {
        "id": "M7", "name": "Email collection",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "4-Polish", "category": "Marketing",
        "blocks": "M9", "blocked_by": "R20, M3",
        "done_when": "Coming-soon page live (Hebrew), collecting emails from interested parents. Integrated with email tool."
    },
    {
        "id": "M8", "name": "SEO & blog content",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Marketing",
        "blocks": "", "blocked_by": "M3, R26, D22",
        "done_when": "Hebrew keyword research done. First 5+ blog posts written and published."
    },
    {
        "id": "M9", "name": "Beta recruitment",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "5-Launch", "category": "Marketing",
        "blocks": "M10", "blocked_by": "M6, M7, P10, R22",
        "done_when": "30-50 Israeli families recruited: coding communities, parenting forums, schools, social media, influencer referrals"
    },
    {
        "id": "M10", "name": "Beta onboarding & feedback",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "5-Launch", "category": "Marketing",
        "blocks": "M11", "blocked_by": "M9",
        "done_when": "Beta families onboarded, feedback forms/interviews set up, weekly feedback collected, NPS measured"
    },
    {
        "id": "M11", "name": "Influencer/blogger partnerships",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "5-Launch", "category": "Marketing",
        "blocks": "M13", "blocked_by": "M3, M6",
        "done_when": "5-10 Israeli parenting influencers/bloggers identified, relationship built, launch collaboration agreed"
    },
    {
        "id": "M12", "name": "Price validation",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "5-Launch", "category": "Payments",
        "blocks": "M13", "blocked_by": "M10, P2",
        "done_when": "Willingness-to-pay tested with beta families. Basic vs Premium uptake measured. Pricing adjusted if needed."
    },
    {
        "id": "M13", "name": "Launch campaign",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "5-Launch", "category": "Marketing",
        "blocks": "", "blocked_by": "M10, M11, M12, D21, R22",
        "done_when": "Full plan: email blast to list, social media blitz, influencer posts, press outreach. Executed on launch day."
    },
    {
        "id": "M14", "name": "Press outreach",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P3-Low", "phase": "5-Launch", "category": "Marketing",
        "blocks": "", "blocked_by": "M13",
        "done_when": "Israeli tech/education media contacted. Press release distributed. Coverage secured."
    },
    {
        "id": "M15", "name": "Community setup",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "5-Launch", "category": "Support",
        "blocks": "", "blocked_by": "M10",
        "done_when": "WhatsApp group or Discord for parents + kids. Moderation guidelines. Community manager."
    },
    {
        "id": "M16", "name": "Customer testimonials",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "5-Launch", "category": "Marketing",
        "blocks": "M13", "blocked_by": "M10",
        "done_when": "Video or written testimonials from beta parents AND kids. Case studies."
    },
    {
        "id": "M17", "name": "Referral mechanism",
        "department": "Marketing", "owner": "Alon", "status": "Backlog",
        "priority": "P3-Low", "phase": "5-Launch", "category": "Marketing",
        "blocks": "", "blocked_by": "R20, R2",
        "done_when": "Simple referral tracking: unique links, 'invite a friend' CTA in platform, reward for referrer"
    },

    # ═══ SUPPORT (CS1-CS8) ═══
    {
        "id": "CS1", "name": "FAQ page content",
        "department": "Support", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Support",
        "blocks": "R20", "blocked_by": "P1, P2, P8",
        "done_when": "20-30 common questions answered in Hebrew: account, billing, platform usage, technical issues, safety"
    },
    {
        "id": "CS2", "name": "Support email setup",
        "department": "Support", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "1-Foundation", "category": "Support",
        "blocks": "CS3", "blocked_by": "",
        "done_when": "Dedicated support email, auto-responder with FAQ link, ticket tracking (even a simple spreadsheet)"
    },
    {
        "id": "CS3", "name": "Response templates",
        "department": "Support", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Support",
        "blocks": "", "blocked_by": "CS1, CS2",
        "done_when": "Pre-written Hebrew responses for common issues: can't login, payment failed, code won't run, cancel subscription, child forgot password"
    },
    {
        "id": "CS4", "name": "'Report Issue' flow",
        "department": "Support", "owner": "Matan", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Support",
        "blocks": "", "blocked_by": "R1",
        "done_when": "In-platform button that sends bug report with context (current page, browser, user ID) to support email"
    },
    {
        "id": "CS5", "name": "Beta feedback process",
        "department": "Support", "owner": "Alon", "status": "Backlog",
        "priority": "P1-High", "phase": "5-Launch", "category": "Support",
        "blocks": "M10", "blocked_by": "P10",
        "done_when": "Feedback forms ready, interview script prepared, feedback tracking system (spreadsheet or Notion), weekly summary to team"
    },
    {
        "id": "CS6", "name": "Escalation process",
        "department": "Support", "owner": "Alon", "status": "Backlog",
        "priority": "P2-Medium", "phase": "4-Polish", "category": "Support",
        "blocks": "", "blocked_by": "CS2",
        "done_when": "Defined: marketer handles L1 (account, billing, basic). Developer handles L2 (bugs, technical). Response time targets (<24hr)."
    },
    {
        "id": "CS7", "name": "Community moderation guidelines",
        "department": "Support", "owner": "Alon", "status": "Backlog",
        "priority": "P3-Low", "phase": "5-Launch", "category": "Support",
        "blocks": "M15", "blocked_by": "P1",
        "done_when": "Rules for WhatsApp/Discord: what's allowed, how to handle conflicts, when to escalate, kid safety rules"
    },
    {
        "id": "CS8", "name": "Knowledge base / help articles",
        "department": "Support", "owner": "Alon", "status": "Backlog",
        "priority": "P3-Low", "phase": "4-Polish", "category": "Support",
        "blocks": "", "blocked_by": "CS1, R5, R3",
        "done_when": "10-15 short help articles: how to use the editor, how hints work, how to upgrade to premium, parent dashboard guide"
    },
]


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Create VRT Feature Board in Notion")
    parser.add_argument("--token", help="Notion API token (or set NOTION_API_KEY env var)")
    parser.add_argument("--dry-run", action="store_true", help="Print tasks without creating anything")
    args = parser.parse_args()

    token = args.token or os.environ.get("NOTION_API_KEY")
    if not token and not args.dry_run:
        print("ERROR: No Notion API token provided.")
        print("  Use --token secret_xxx or set NOTION_API_KEY env var")
        print("  Use --dry-run to preview tasks without Notion access")
        sys.exit(1)

    print(f"VRT Feature Board — {len(TASKS)} tasks to create")
    print()

    if args.dry_run:
        for t in TASKS:
            print(f"  [{t['id']}] {t['name']}  |  {t['department']} / {t['owner']}  |  {t['phase']} / {t['priority']}  |  {t['category']}")
        print(f"\nTotal: {len(TASKS)} tasks")
        return

    # Step 1: Create database
    db_id = create_database(token)
    time.sleep(RATE_LIMIT_DELAY)

    # Step 2: Populate tasks
    print(f"\nPopulating {len(TASKS)} tasks...")
    success = 0
    errors = 0
    for i, task in enumerate(TASKS):
        try:
            add_task(token, db_id, task)
            success += 1
            print(f"  [{i+1}/{len(TASKS)}] {task['id']}: {task['name']}")
        except Exception as e:
            errors += 1
            print(f"  [{i+1}/{len(TASKS)}] FAILED {task['id']}: {task['name']} — {e}")
        time.sleep(RATE_LIMIT_DELAY)

    print(f"\nDone! {success} created, {errors} errors")
    print(f"Database ID: {db_id}")
    print(f"Open in Notion: https://notion.so/{db_id.replace('-', '')}")

    # Step 3: Verify
    print("\nVerifying...")
    time.sleep(1)
    try:
        result = notion_request("POST", f"databases/{db_id}/query", token, {"page_size": 1})
        total = result.get("results", [])
        has_more = result.get("has_more", False)
        print(f"  Query returned {len(total)} result(s), has_more={has_more}")
        if total:
            first = total[0]["properties"]
            name = first["Name"]["title"][0]["text"]["content"] if first["Name"]["title"] else "?"
            tid = first["Task ID"]["rich_text"][0]["text"]["content"] if first["Task ID"]["rich_text"] else "?"
            print(f"  Sample entry: {tid} — {name}")
    except Exception as e:
        print(f"  Verification failed: {e}")


if __name__ == "__main__":
    main()
