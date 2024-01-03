#!/bin/bash

# useful to reset history when it's too big
# the git history in this context is not very important

rm -rf .git

git init
git add .
git commit -m "Initial commit"

git remote add origin git@github.com:Bel-Art/telecom-logos.git
git push -u --force origin main
