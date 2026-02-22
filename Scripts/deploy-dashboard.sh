#!/bin/bash
# VRT Dashboard — one-click regenerate + deploy
# Usage: bash ~/Desktop/Alon-Workspace/Scripts/deploy-dashboard.sh

set -e

WORKSPACE="${HOME}/Desktop/Alon-Workspace"
DASH_REPO="${WORKSPACE}/.dashboard-deploy"

echo "Regenerating dashboard from Notion..."
VRT_NO_OPEN=1 python3 "${WORKSPACE}/Scripts/generate-dashboard.py"

# Clone dashboard repo if not present
if [ ! -d "$DASH_REPO" ]; then
  echo "Cloning vrt-dashboard repo..."
  git clone https://github.com/alondotb/vrt-dashboard.git "$DASH_REPO"
fi

echo "Deploying to GitHub Pages..."
cp "${WORKSPACE}/Docs/dashboard.html" "${DASH_REPO}/"
cp "${WORKSPACE}/Docs/index.html" "${DASH_REPO}/"
cd "$DASH_REPO"
git add -A
git commit -m "Dashboard update $(date '+%Y-%m-%d %H:%M')" || echo "No changes to commit"
git push origin main

echo "Live at https://alondotb.github.io/vrt-dashboard/"
