# 🚀 archpkg-helper 

**archpkg-helper** is a CLI tool to search and generate install commands for Linux packages from multiple sources:
- Arch Linux official repositories (pacman)
- Arch User Repository (AUR)
- Flatpak (flathub)

It helps you find packages and provides the correct install command for your system.

## 📌 Project Overview
archpkg-helper simplifies searching and installing Linux packages across multiple sources. It provides an interactive CLI to quickly find packages, filter results, and generate the appropriate installation commands for your system.


## ✨ Features
- Search for packages by name or description.
- Supports pacman, AUR, and Flatpak sources.
- Fuzzy matching and filtering for best results.
- Interactive selection and install command generation.

## 🛠 Requirements
- **Python 3.6+**
- Libraries (installed automatically):
    -`requests`, `rich`, `fuzzywuzzy`, `python-Levenshtein` 
- For full functionality:
  - Arch Linux: `pacman`, `yay` (AUR helper)
  - Any distro: `flatpak` (for Flatpak support)

## ⚙️  Installation Guide

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

## ▶️ Usage

Search for a package:
```sh
archpkg <package-name>
```
Example:
```sh
archpkg firefox
```

## 📂 Project Structure

```bash
__pycache__
archpkg.cpython-313.pyc
├──command_gen.cpython-313.pyc
├──search_aur.cpython-313.pyc
├──search_flatpak.cpython-313.pyc
├──search_pacman.cpython-313.pyc
archpkg_helper.egg-info
├──dependency_links.txt
├──entry_points.txt
├──PKG-INFO
├──requires.txt
├──SOURCES.txt
├──top_level.txt
build/lib
├──archpkg.py
├──command_gen.py
├──search_aur.py
├──search_flatpak.py
├──search_pacman.py
CODE_OF_CONDUCT.md
CONTRIBUTING.md
LICENSE
README.md
archpkg.py
command_gen.py
search_aur.py
search_flatpak.py
search_pacman.py
setup.py

```
## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository
2. Create a new branch (git checkout -b feature-name)
3. Make your changes
4. Commit your changes (git commit -m 'Add feature')
5. Push to the branch  (git push origin feature-name)
6. Create a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## 📧 Contact  

For queries, feedback, or guidance regarding this project, you can contact the **mentor** assigned to the issue:  

- 📩 **GitHub**: [AdmGenSameer](https://github.com/AdmGenSameer)
- 💬 **By commit/PR comments**: Please tag the mentor in your commit or pull request discussion for direct feedback.  
 
Original Repository: [archpkg-helper](https://github.com/AdmGenSameer/archpkg-helper.git) 



## 📄 **License**
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

--- 
