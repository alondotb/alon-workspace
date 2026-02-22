# VRT Workspace Map

> Single source of truth for where everything lives — locally and in Notion.
> Last updated: 2026-02-18

---

## Hierarchy

```
Alon (person)
  └── Alon-Workspace/  (~/Desktop/Alon-Workspace/)
        ├── CLAUDE.md               ← Workspace rules for Claude Code
        ├── tools.json              ← Tool inventory (synced from Notion)
        │
        ├── Docs/                   ← Documentation & reference
        │     ├── workspace-map.md          ← THIS FILE
        │     ├── VRT-Visual-Identity.md    ← Visual identity v1.1 (colors, type, motion)
        │     ├── brand-brief.md            ← Brand personality, voice, color palette
        │     ├── RnD_Feature_Breakdown.md  ← R&D feature specs for Matan
        │     ├── links.md                  ← All URLs, tools, accounts
        │     ├── dashboard.html            ← Generated VRT dashboard
        │     ├── marketing-launch-plan.md  ← Marketing plan
        │     ├── market-research-plan.md   ← Market research playbook
        │     └── design-specs/             ← Figma PRD design specs (12 files)
        │           ├── 00-overview.md
        │           ├── 01-auth-onboarding.md
        │           ├── 02-learning-core.md
        │           ├── 03-projects.md
        │           ├── 04-gamification.md
        │           ├── 05-social.md
        │           ├── 06-bug-hunt.md
        │           ├── 07-parent-dashboard.md
        │           ├── 08-payments-trial.md
        │           ├── 09-marketing-pages.md
        │           ├── 10-emails.md
        │           └── 11-navigation-components.md
        │
        ├── Visuals/                ← All visual assets
        │     ├── brand/
        │     │     └── VRT_LOGO.png        ← Primary logo
        │     ├── campaign-tree-nodes/
        │     │     ├── adventurer-character-1.png
        │     │     └── adventurer-character-3.png
        │     ├── ui-concepts/
        │     │     ├── ui-showcase-0.png
        │     │     ├── ui-showcase-1.png
        │     │     ├── ui-showcase-2.png
        │     │     └── ui-showcase-3.png
        │     ├── Lesson_Terminal.png
        │     ├── lesson_01.png
        │     └── PROMPTS_CLEAN.txt         ← Midjourney prompt reference
        │
        ├── Alon - Renders/         ← 3D animation renders (Blender)
        │     ├── cubes_00.blend
        │     ├── VIDEO-010001-0250.mp4
        │     └── [PNG's]/                  ← 250 render frames
        │
        ├── Scripts/                ← Automation
        │     ├── generate-dashboard.py     ← Dashboard generator (Notion → HTML)
        │     ├── dashboard-server/         ← Express server for chat + live dashboard
        │     │     ├── server.js
        │     │     └── package.json
        │     ├── file-viewer/              ← Local file browser (Express)
        │     └── (other utility scripts)
        │
        └── Marketing-Handoff/      ← Assets for Sahar
```

---

## Notion Mirror

Every key local doc has a Notion counterpart:

| Local File | Notion Location | Purpose |
|------------|----------------|---------|
| `CLAUDE.md` | — (local only) | Claude Code workspace rules |
| `tools.json` | Tool Inventory DB | Machine-readable tool list |
| `Docs/VRT-Visual-Identity.md` | Workspace - VRT / Visual Identity | Brand colors, type, motion spec |
| `Docs/brand-brief.md` | Workspace - VRT / Brand Brief | Personality, voice, palette |
| `Docs/RnD_Feature_Breakdown.md` | Workspace - VRT / R&D Features | Feature specs for dev |
| `Docs/links.md` | — (local only, quick-access) | URLs and account reference |
| `Docs/design-specs/*` | Workspace - VRT / Design Specs | Figma PRD source docs |
| `Docs/dashboard.html` | — (generated, served via Netlify) | Live dashboard |

---

## Notion Databases

| Database | ID | What's in it |
|----------|-----|-------------|
| VRT Tracker | `30a5308b-6bc5-8171-...` | Goals, Projects, Tasks (all 3 planes) |
| Feature Board | `30a5308b-6bc5-814f-...` | Granular dev tasks linked to Tracker |
| Tool Inventory | `3408692e-ca14-4886-...` | All 16 tools with connections |

---

## Visual Identity Files — Where Each Goes

| Asset Type | Local Location | Figma | Notion |
|-----------|---------------|-------|--------|
| Logo (PNG/SVG) | `Visuals/brand/` | Figma Brand Kit page | Workspace - VRT |
| Color palette | `Docs/brand-brief.md` | Figma color styles | Brand Brief page |
| Typography spec | `Docs/VRT-Visual-Identity.md` | Figma text styles | Visual Identity page |
| Character art | `Visuals/campaign-tree-nodes/` | Figma asset library | — |
| UI mockups | `Visuals/ui-concepts/` | Figma design files | — |
| Screen designs | — | Figma (primary home) | Design Specs pages |
| 3D renders | `Alon - Renders/` | — | — |
| Midjourney prompts | `Visuals/PROMPTS_CLEAN.txt` | — | — |
| Design specs | `Docs/design-specs/` | Referenced in Figma | Design Specs pages |

---

## Design Pipeline Flow

```
Google Stitch / Lovable  →  Figma  →  Design Specs (.md)  →  R&D (Matan)
     (visual design)      (cleanup)   (PRD docs)              (code)
```

1. **Design** in Google Stitch + Lovable (rapid visual prototyping)
2. **Export** to Figma (component cleanup, style extraction)
3. **Document** in `Docs/design-specs/` (PRD for R&D)
4. **Hand off** to Matan via Feature Board + component specs

---

## Projects with Separate Repos (planned)

| Project | Repo Name | Status |
|---------|-----------|--------|
| VRT Landing Page | `vrt-landing` | Planned |
| VRT Platform | `vrt-platform` | Planned |
| VRT Dashboard | `vrt-dashboard` | Live on Netlify |
| Miki AI | `miki-ai` | Planned |

All under the `alon-main` GitHub account/org.
