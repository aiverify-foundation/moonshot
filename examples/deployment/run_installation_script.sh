# install moonshot
pip3 install --no-cache-dir "aiverify-moonshot[all]"

# install moonshot-data and moonshot-ui
python -m moonshot -i moonshot-data -i moonshot-ui

# start moonshot web
python -m moonshot web
