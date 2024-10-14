# set logger
export MS_LOG_NAME="moonshot"
export MS_LOG_LEVEL="DEBUG"
export MS_LOG_TO_FILE="true"

# install moonshot
pip3 install --no-cache-dir "aiverify-moonshot[all]"

# install in /app/data
cd /app/data

# install moonshot-data and moonshot-ui
python -m moonshot -i moonshot-data -u
python -m moonshot -i moonshot-ui -u

# start moonshot web
python -m moonshot web
