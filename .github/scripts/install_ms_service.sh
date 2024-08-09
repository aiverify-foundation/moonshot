!/bin/bash

# Check if branch name is provided, default to dev_main if not
BRANCH_NAME=${1:-dev_main}

# Install moonshot from GitHub

cd ~/moonshot

# Clone the repositories from the specified branch
git clone --branch $BRANCH_NAME https://github.com/aiverify-foundation/moonshot.git
cd moonshot
git clone --branch $BRANCH_NAME https://github.com/aiverify-foundation/moonshot-data.git
git clone --branch $BRANCH_NAME https://github.com/aiverify-foundation/moonshot-ui.git
cp ~/scripts/.env .

python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
cd moonshot-data
pip install -r requirements.txt

# Install Node.js dependencies and build the UI
cd ../moonshot-ui
npm install
npm run build
