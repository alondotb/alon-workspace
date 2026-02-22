# VRT Dashboard

Live operational dashboard for Virtual Techies Phase 0 (Feb 18 – Mar 8, 2026).

## Files in this folder

| File | Purpose |
|------|---------|
| `structural-brief.md` | Layout blueprint for Lovable redesign (no visual decisions) |
| `functionality-spec.md` | Full functionality spec (architecture, API, sections, interactions) |
| `visual-design.md` | Visual design spec (colors, type, components, animations) |

The generated dashboard HTML lives at `Docs/dashboard.html` (output of the Python generator).

## How to refresh

Data comes from the Notion VRT Tracker. To regenerate:

```bash
python3 ~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py
```

Auto-refreshes in-browser every 60 seconds. Live at https://vrt-dashboard.netlify.app

## Team

| Person | Role |
|--------|------|
| Alon | Product, Design, Business |
| Matan | R&D, Development |
| Sahar | Marketing |
