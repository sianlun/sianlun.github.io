#!/bin/bash
# Quick deploy script for sianlun.github.io
# Usage: ./deploy.sh "your commit message"

MSG="${1:-Update site content}"

cd "$(dirname "$0")"

git add -A
git commit -m "$MSG"
git push origin main

echo ""
echo "Pushed to main. GitHub Actions will deploy to Pages automatically."
echo "Check status: https://github.com/sianlun/sianlun.github.io/actions"
