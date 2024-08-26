#!/bin/bash

# Check if branch name is provided, default to dev_main if not
BRANCH_NAME=${1:-dev_main}

BASE_DIR=~/moonshot
SCRIPTS_DIR=~/scripts
#BASE_DIR=./moonshot-test
#SCRIPTS_DIR=./.github/scripts

MOONSHOT_SIT=moonshot-sit

# Install moonshot from GitHub

# Create BASE_DIR if it does not
if [ ! -d "$BASE_DIR" ]; then
  mkdir -p "$BASE_DIR"
fi

cd $BASE_DIR

# Clone the repositories from the specified branch
git clone --branch $BRANCH_NAME https://github.com/aiverify-foundation/moonshot.git $MOONSHOT_SIT
cd $MOONSHOT_SIT
git clone --branch $BRANCH_NAME https://github.com/aiverify-foundation/moonshot-data.git
git clone --branch $BRANCH_NAME https://github.com/aiverify-foundation/moonshot-ui.git
cp $SCRIPTS_DIR/moonshot_env .env

python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
cd moonshot-data
pip install -r requirements.txt

# Install Node.js dependencies and build the UI
cd ../moonshot-ui
rm .env.local
cp $SCRIPTS_DIR/moonshot_ui_env .env.local
npm install

# Modify the start script in package.json
sudo apt-get install -y jq
jq '.scripts.start = "next start -H 0.0.0.0 -p 3100"' package.json > package.tmp.json && mv package.tmp.json package.json

npm run build
