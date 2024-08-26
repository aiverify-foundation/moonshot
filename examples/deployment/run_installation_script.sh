# install moonshot
pip3 install --no-cache-dir "aiverify-moonshot[all]"

# install in /app/data
cd /app/data

# install moonshot-data and moonshot-ui
python -m moonshot -i moonshot-data -i moonshot-ui

# start moonshot web
python -m moonshot web
