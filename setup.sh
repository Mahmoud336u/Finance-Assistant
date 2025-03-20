#!/bin/bash

# setup.sh - AI-Driven Personal Finance Assistant Setup Script

# Exit on error and show commands
set -xe

# ---- Configuration ----
PYTHON_VERSION="3.10.12"
VENV_NAME="finance-env"
REQUIREMENTS_FILE="requirements.txt"
AWS_CONFIG_DIR="$HOME/.aws"
AWS_CREDENTIALS_FILE="$AWS_CONFIG_DIR/credentials"

# ---- System Setup ----
echo -e "\033[1;34mChecking system dependencies...\033[0m"

# Check for Python 3.10
if ! command -v python3.10 &> /dev/null; then
    echo -e "\033[1;31mPython 3.10 not found. Installing...\033[0m"
    
    # For Debian/Ubuntu systems
    sudo apt-get update
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get install -y python3.10 python3.10-venv python3.10-dev
    
    # Install pyenv alternative if needed
    if ! command -v python3.10 &> /dev/null; then
        echo -e "\033[1;33mUsing pyenv to install Python 3.10...\033[0m"
        curl https://pyenv.run | bash
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init --path)"
        pyenv install $PYTHON_VERSION
        pyenv global $PYTHON_VERSION
    fi
fi

# ---- Virtual Environment ----
echo -e "\033[1;34mSetting up virtual environment...\033[0m"

# Remove existing environment if it exists
if [ -d "$VENV_NAME" ]; then
    echo -e "\033[1;33mRemoving existing virtual environment...\033[0m"
    rm -rf $VENV_NAME
fi

# Create fresh environment
python3.10 -m venv $VENV_NAME

# Activate environment
source $VENV_NAME/bin/activate

# ---- Dependency Installation ----
echo -e "\033[1;34mInstalling Python dependencies...\033[0m"

# Upgrade pip first
python -m pip install --upgrade pip

# Install exact versions from requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r $REQUIREMENTS_FILE
else
    echo -e "\033[1;31mError: $REQUIREMENTS_FILE not found!\033[0m"
    exit 1
fi

# ---- AWS Configuration Check ----
echo -e "\033[1;34mChecking AWS configuration...\033[0m"

if [ ! -d "$AWS_CONFIG_DIR" ]; then
    echo -e "\033[1;33mCreating AWS config directory...\033[0m"
    mkdir -p $AWS_CONFIG_DIR
fi

if [ ! -f "$AWS_CREDENTIALS_FILE" ]; then
    echo -e "\033[1;33mAWS credentials not found. You'll need to:"
    echo -e "1. Run 'aws configure' after setup"
    echo -e "2. Set up credentials for AWS services\033[0m"
fi

# ---- Post-Installation ----
echo -e "\033[1;32mSetup completed successfully!\033[0m"
echo -e "\nTo activate the virtual environment:"
echo -e "source $VENV_NAME/bin/activate"
echo -e "\nTo verify AWS configuration:"
echo -e "aws sts get-caller-identity"

# ---- Clean Exit ----
exit 0
