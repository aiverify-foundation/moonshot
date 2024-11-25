activate () {
  . ./env/bin/activate
}

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python could not be found. Please install Python and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found. Please install pip and try again."
    exit 1
fi

# Create a virtual environment
python3 -m venv env
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate the virtual environment
activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install the moonshot requirements
pip3 install -r ../../requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install requirements from ../requirements.txt."
    deactivate
    exit 1
fi

# Install rich library for display
pip3 install rich
if [ $? -ne 0 ]; then
    echo "Failed to install rich library."
    deactivate
    exit 1
fi

# Clone moonshot data and install its requirements
git clone https://github.com/aiverify-foundation/moonshot-data.git
if [ $? -ne 0 ]; then
    echo "Failed to clone moonshot-data repository."
    deactivate
    exit 1
fi

pip install -r moonshot-data/requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install requirements from moonshot-data/requirements.txt."
    deactivate
    exit 1
fi

# Create the jupyter notebook server in the virtual environment
ipython kernel install --user --name=env
if [ $? -ne 0 ]; then
    echo "Failed to create Jupyter notebook server."
    deactivate
    exit 1
fi

# Launch Jupyter notebook
jupyter notebook
if [ $? -ne 0 ]; then
    echo "Failed to launch Jupyter notebook."
    deactivate
    exit 1
fi