# archpkg-helper

**archpkg-helper** is a CLI tool to search and generate install commands for Linux packages from multiple sources:
- Arch Linux official repositories (pacman)
- Arch User Repository (AUR)
- Flatpak (flathub)

It helps you find packages and provides the correct install command for your system.

## Features
- Search for packages by name or description.
- Supports pacman, AUR, and Flatpak sources.
- Fuzzy matching and filtering for best results.
- Interactive selection and install command generation.

## Requirements
- Python 3.6+
- `requests`, `rich`, `fuzzywuzzy`, `python-Levenshtein` (installed automatically)
- For full functionality:
  - Arch Linux: `pacman`, `yay` (AUR helper)
  - Any distro: `flatpak` (for Flatpak support)

---

## Installation Guide

### 1. Install Python and pip
Make sure you have Python 3 and pip installed:
```sh
python3 --version
pip3 --version
```

### 2. Clone the repository
```sh
git clone https://github.com/AdmGenSameer/archpkg-helper.git
cd archpkg-helper
```

### 3. Install the package
```sh
pip install .
```
Or for development:
```sh
pip install -e .
```

### 4. Install system dependencies

#### Arch Linux / Manjaro
- `pacman` is pre-installed.
- Install `yay` for AUR support:
  ```sh
  sudo pacman -S yay
  ```
- Install `flatpak` if needed:
  ```sh
  sudo pacman -S flatpak
  ```

#### Ubuntu / Linux Mint / Debian
- Install `flatpak`:
  ```sh
  sudo apt update
  sudo apt install flatpak
  ```
- For AUR support, you need an Arch-based system or use only Flatpak.

#### Fedora
- Install `flatpak`:
  ```sh
  sudo dnf install flatpak
  ```
- For AUR support, you need an Arch-based system or use only Flatpak.

#### openSUSE
- Install `flatpak`:
  ```sh
  sudo zypper install flatpak
  ```

---

## Usage

Search for a package:
```sh
archpkg <package-name>
```
Example:
```sh
archpkg firefox
```
Follow the interactive prompts to select and install the package.

---
