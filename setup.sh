#!/bin/bash

# Moonshot automated installation script (using uv)
# Usage: chmod +x setup.sh && ./setup.sh

set -e  # Exit immediately if a command exits with a non-zero status

echo "========================================="
echo "Moonshot installation script (uv version)"
echo "========================================="

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check whether uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed${NC}"
    echo "Please install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo -e "${GREEN}✓ uv is installed${NC}"

# Set Python version
PYTHON_VERSION="3.11"
PROJECT_DIR="moonshot-project"

# Create project directory
echo -e "${YELLOW}Creating project directory: $PROJECT_DIR${NC}"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create virtual environment
echo -e "${YELLOW}Creating Python $PYTHON_VERSION virtual environment...${NC}"
uv venv --python "$PYTHON_VERSION"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Initialize project
echo -e "${YELLOW}Initializing project...${NC}"
uv init

# Install Moonshot
echo -e "${YELLOW}Installing aiverify-moonshot[all]...${NC}"
uv pip install "aiverify-moonshot[all]"

# Install pip compatibility layer
echo -e "${YELLOW}Installing pip compatibility layer...${NC}"
uv pip install pip

# Run Moonshot initialization
echo -e "${YELLOW}Initializing Moonshot data and UI...${NC}"
uv run python -m moonshot -i moonshot-data -i moonshot-ui

echo -e "${GREEN}========================================="
echo "✅ Moonshot installation complete!"
echo "=========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Change into the project directory: cd $PROJECT_DIR"
echo "2. Activate the environment: source .venv/bin/activate"
echo "3. Start the Web UI: uv run python -m moonshot web"
echo ""
echo "Or start directly:"
echo "cd $PROJECT_DIR && source .venv/bin/activate && uv run python -m moonshot web"
