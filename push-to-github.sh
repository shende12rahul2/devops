#!/usr/bin/env bash
# Push DevOps Mastery repo to GitHub
# Usage: ./push-to-github.sh
# Prerequisites: git configured with your GitHub credentials

set -euo pipefail

REPO_URL="https://github.com/shende12rahul2/devops.git"
REPO_DIR="$(dirname "$0")"

echo "=== Pushing DevOps Mastery to GitHub ==="
echo ""

cd "$REPO_DIR"

# Init git if needed
if [ ! -d ".git" ]; then
    git init
    git remote add origin "$REPO_URL"
    echo "✓ Git initialized"
fi

# Configure git
git config user.email "$(git config --global user.email 2>/dev/null || echo 'your@email.com')"
git config user.name "$(git config --global user.name 2>/dev/null || echo 'Rahul Shende')"

# Stage all
git add -A

# Commit
COMMIT_MSG="chore: initialize devops mastery roadmap repo

- Full 36-week learning structure (1440 hours)
- Phase 1-5 with labs, projects, interview prep
- Enterprise-grade project deliverables
- CNCF tools learning map
- Streamlit progress tracker
- GitHub Actions CI workflow"

git commit -m "$COMMIT_MSG" || echo "Nothing to commit"

# Push
git branch -M main
git push -u origin main --force

echo ""
echo "✅ Pushed to: $REPO_URL"
echo ""
echo "Next steps:"
echo "1. Visit https://github.com/shende12rahul2/devops"
echo "2. Add a description: 'DevOps Mastery — 36-week journey to senior/staff level'"
echo "3. Add topics: devops, kubernetes, sre, platform-engineering, cncf"
echo "4. Pin the repo on your GitHub profile"
