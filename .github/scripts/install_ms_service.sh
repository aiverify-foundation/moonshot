#!/bin/bash

# Arguments for branches, default to dev_main if not provided.
MOONSHOT_BRANCH=${1:-dev_main}
MOONSHOT_DATA_BRANCH=${2:-dev_main}
MOONSHOT_UI_BRANCH=${3:-dev_main}

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

# Clone the repositories from the specified branches
echo "Cloning moonshot from branch $MOONSHOT_BRANCH"
echo "Cloning moonshot-data from branch $MOONSHOT_DATA_BRANCH"
echo "Cloning moonshot-ui from branch $MOONSHOT_UI_BRANCH"
git clone --branch $MOONSHOT_BRANCH https://github.com/aiverify-foundation/moonshot.git $MOONSHOT_SIT
cd $MOONSHOT_SIT
git clone --branch $MOONSHOT_DATA_BRANCH https://github.com/aiverify-foundation/moonshot-data.git
git clone --branch $MOONSHOT_UI_BRANCH https://github.com/aiverify-foundation/moonshot-ui.git
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
