#!/bin/sh
# Install the pre-commit hook that moves new chapters automatically
HOOK_DIR="$(git rev-parse --git-dir)/hooks"
cp scripts/pre-commit "$HOOK_DIR/pre-commit"
chmod +x "$HOOK_DIR/pre-commit"
echo "Installed pre-commit hook to $HOOK_DIR/pre-commit"
