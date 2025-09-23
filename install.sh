#!/bin/bash

set -e

echo "[*] Installing ArchPkg CLI..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[*] Python3 not found. Installing..."
    if [ -f /etc/debian_version ]; then
        sudo apt update && sudo apt install -y python3 python3-pip
    elif [ -f /etc/redhat-release ]; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python python-pip
    else
        echo "[!] Unsupported distro. Please install Python3 manually."
        exit 1
    fi
fi

# Install pip if missing
if ! command -v pip3 &> /dev/null; then
    echo "[*] pip not found. Installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
fi


# Check for pipx
if ! command -v pipx &> /dev/null; then
    echo "[*] pipx not found. Installing..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-pipx
    else
        python3 -m pip install --user pipx
        python3 -m pipx ensurepath
    fi
fi

# Install ArchPkg CLI with pipx from current directory
pipx install .

echo "[✔] ArchPkg installed via pipx. Run with: archpkg"
