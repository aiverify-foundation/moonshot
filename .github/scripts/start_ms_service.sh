!/bin/bash

BASE_DIR=~/moonshot
MOONSHOT_SIT=moonshot-sit

cd $BASE_DIR/$MOONSHOT_SIT

source venv/bin/activate
python -m moonshot web

