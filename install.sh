#!/bin/bash

set -e

echo "[*] Installing ArchPy CLI..."

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

# Install archpy
pip3 install archpy

echo "[✔] ArchPy installed. Run with: archpy"
