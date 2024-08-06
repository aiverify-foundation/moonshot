# Use an official Python runtime as a parent image
FROM python:3.11-slim AS build

# patches & OS dependencies
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y git build-essential pkg-config libhdf5-dev npm && \
    rm -rf /var/lib/apt/lists/*

# python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    #pip3 install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple "aiverify-moonshot-eks[all]==0.1.0" && \
    #pip3 install --no-cache-dir "aiverify-moonshot[all]" && \
    pip3 install --no-cache-dir h5py

# install moonshot-data and moonshot-ui
# RUN python -m moonshot -i moonshot-data -i moonshot-ui

# temporary clone moonshot and install from source
WORKDIR /app
COPY . .
RUN git clone -b ms-353 https://github.com/aiverify-foundation/moonshot.git && \
    cd moonshot && \
    pip3 install --no-cache-dir -r requirements.txt
RUN cd moonshot && \
    python -m moonshot -i moonshot-data -i moonshot-ui
RUN cp ms-env.env moonshot/.env && \
    cp ms-ui-env.env moonshot/moonshot-ui/.env

# expose the port the app runs on
EXPOSE 3000

# run cmd
CMD ["sh", "-c", "cd /app/moonshot && python -m moonshot web"]

