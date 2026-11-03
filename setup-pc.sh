#!/usr/bin/env bash
# One-time setup of a PC for my Claude: shared files, /ticket skill, tickets.
# Safe to run again. In Git Bash:
#   curl -fsSL https://raw.githubusercontent.com/Thanathors/tickets-app/main/setup-pc.sh | bash
set -e

command -v git >/dev/null || { echo "Install Git for Windows first: https://git-scm.com/download/win"; exit 1; }
if python -c "" 2>/dev/null; then PY=python
elif py -3 -c "" 2>/dev/null; then PY="py -3"
else echo "Install Python 3 first: https://www.python.org/downloads/ (tick 'Add to PATH')"; exit 1; fi

for repo in claude-shared tickets; do
  if [ -d ~/$repo/.git ]; then
    echo "Updating ~/$repo"; git -C ~/$repo pull --ff-only -q
  else
    echo "Getting ~/$repo (sign in to GitHub if asked)"; git clone -q https://github.com/Thanathors/$repo.git ~/$repo
  fi
  git -C ~/$repo config user.name "Thanathors"
  git -C ~/$repo config user.email "Thanathors@users.noreply.github.com"
done

$PY ~/claude-shared/setup.py
echo; echo "Your tickets:"; $PY ~/tickets/tickets.py list
echo; echo "All set. Restart Claude, then say \"sync\" whenever you switch PCs."
