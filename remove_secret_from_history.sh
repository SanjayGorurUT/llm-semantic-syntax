#!/bin/bash
# Script to remove API keys from git history
# WARNING: This rewrites git history. Only use if you're the only one working on this branch.

echo "⚠️  WARNING: This will rewrite git history!"
echo "Make sure you're the only one working on this branch."
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Find the commit with the secret
COMMIT_HASH="2ee51650889b5cb553dbe25ee69f43a2dcf77474"

echo "Removing secrets from git history..."
echo ""

# Method 1: Use git filter-branch to remove the file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch test_apis.py" \
  --prune-empty --tag-name-filter cat -- --all

# Alternative: If you want to remove the entire commit
# git rebase -i ${COMMIT_HASH}^
# Then mark the commit for deletion

echo ""
echo "✅ Git history cleaned!"
echo ""
echo "Next steps:"
echo "1. Review the changes: git log"
echo "2. Force push (if you're sure): git push --force-with-lease"
echo ""
echo "⚠️  Note: If others are working on this repo, coordinate with them first!"

