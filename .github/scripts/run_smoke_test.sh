#!/bin/bash

# Check if branch name is provided, default to dev_main if not
BRANCH_NAME=${1:-main}

cd ~/moonshot

if [ -d "moonshot-smoke-testing" ]; then
  echo "Removing existing moonshot-smoke-testing directory..."
  rm -rf moonshot-smoke-testing
fi

# Clone the smoke test repo from the specified branch
echo "Cloning moonshot-smoke-testing repo from branch $BRANCH_NAME..."
git clone --branch $BRANCH_NAME https://github.com/aiverify-foundation/moonshot-smoke-testing.git
cd moonshot-smoke-testing
npm ci

# Install Playwright (if needed)
#sudo npx playwright install-deps
### If the above didn't work, try the following:
##sudo apt-get install libatk1.0-0\
##         libatk-bridge2.0-0\
##         libxkbcommon0\
##         libatspi2.0-0\
##         libxcomposite1\
##         libxdamage1\
##         libxfixes3\
##         libxrandr2\
##         libgbml

echo "Running smoke test..."
npx playwright test tests/smoke-test.spec.ts --reporter=list

#echo "Exit code: $?"
