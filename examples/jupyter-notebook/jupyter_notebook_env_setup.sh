activate () {
  . ./env/bin/activate
}

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "Python could not be found. Please install Python and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please install pip and try again."
    exit 1
fi

# Create a virtual environment
python -m venv env
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
pip install -r ../../requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install requirements from ../requirements.txt."
    deactivate
    exit 1
fi

# Install supporting libraries
pip install jupyter rich ipython ipykernel
if [ $? -ne 0 ]; then
    echo "Failed to install supporting libraries."
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