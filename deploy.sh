#!/bin/bash
# Quick deployment script for GitHub Pages
# Usage: ./deploy.sh [commit message]

set -e  # Exit on error

echo "🚀 Starting deployment to GitHub Pages..."
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    echo "   Run 'git init' first"
    exit 1
fi

# Build trial data
echo "📦 Building trial data..."
python3 build_data.py
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to build trial data"
    exit 1
fi

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    # Add all files
    echo "📝 Adding files to git..."
    git add .
    
    # Commit with message
    COMMIT_MSG="${1:-Update website: $(date +%Y-%m-%d\ %H:%M:%S)}"
    echo "💾 Committing changes: $COMMIT_MSG"
    git commit -m "$COMMIT_MSG"
    
    # Push to GitHub
    echo "⬆️  Pushing to GitHub..."
    CURRENT_BRANCH=$(git branch --show-current)
    git push origin "$CURRENT_BRANCH"
    
    echo ""
    echo "✅ Deployment complete!"
    echo "   Check GitHub Pages in 1-2 minutes"
    echo "   Repository: $(git remote get-url origin 2>/dev/null || echo 'Not set')"
else
    echo "ℹ️  No changes detected, skipping commit"
fi

echo ""
echo "✨ Done!"

