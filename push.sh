#!/bin/bash

echo "🚀 Pushing commits to GitHub..."
echo ""
echo "📝 You need a GitHub Personal Access Token"
echo "   Create one at: https://github.com/settings/tokens/new"
echo "   Required scope: 'repo'"
echo ""
read -sp "Enter your GitHub token: " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo "❌ Token is empty!"
    exit 1
fi

echo "📤 Pushing to GitHub..."
git push https://${TOKEN}@github.com/archfay/Nexus.git main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ Push failed!"
    exit 1
fi
