# Use an official Python runtime as a parent image
FROM python:3.11-slim AS build

# patches & OS dependencies
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y git build-essential pkg-config libhdf5-dev npm && \
    rm -rf /var/lib/apt/lists/*

# python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir h5py

# Create moonshot user
ARG USER=moonshot
RUN groupadd -g 1000 $USER
RUN useradd -u 1000 -g 1000 -ms /bin/bash $USER

# copy installation script
WORKDIR /app
COPY run_installation_script.sh .

# set executable rights to the installation script
RUN chmod +x /app/run_installation_script.sh

# Create /app/data directory and change owner
RUN mkdir /app/data && chown -R 1000:1000 /app/data

# Change owner
RUN chown -R 1000:1000 /app

# expose the port the app runs on
EXPOSE 3000

# Run containers with non-root user
USER $USER

WORKDIR /app

# Ensure the script is executable and runs correctly
CMD ["sh", "-c", "./run_installation_script.sh"]