#!/bin/bash

AZURE_OPENAI_API_KEY=$1
AZURE_OPENAI_ENDPOINT=$2
TEST_BRANCH_NAME=${3:-main}

BASE_DIR=~/moonshot
SCRIPTS_DIR=~/scripts

# Export the env variables for smoke test to use
export AZURE_OPENAI_TOKEN=$AZURE_OPENAI_API_KEY
export AZURE_OPENAI_URI=$AZURE_OPENAI_ENDPOINT
export MOONSHOT_URL="http://127.0.0.1"
export MOONSHOT_PORT_NUMBER="3100"
export ADDITIONAL_PARAMETERS="{
  'timeout': 300,
  'allow_retries': true,
  'num_of_retries': 3,
  'temperature': 0.5,
  'model': 'gpt-4o'
}"

cd $BASE_DIR

if [ -d "moonshot-smoke-testing" ]; then
  echo "Removing existing moonshot-smoke-testing directory..."
  rm -rf moonshot-smoke-testing
fi

# Clone the smoke test repo from the specified branch
echo "Cloning moonshot-smoke-testing repo from branch $BRANCH_NAME..."
git clone --branch $TEST_BRANCH_NAME https://github.com/aiverify-foundation/moonshot-smoke-testing.git
cd moonshot-smoke-testing
npm ci

cp $SCRIPTS_DIR/moonshot_test_env .env
echo "Created .env"
cat .env

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

echo "Running smoke test on moonshot at $MOONSHOT_URL:$MOONSHOT_PORT_NUMBER..."
npx playwright test tests/smoke-test.spec.ts --reporter=list

#echo "Exit code: $?"
