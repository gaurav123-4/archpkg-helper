# archpkg-helper

A command-line utility for simplifying package management on Linux distributions. This project aims to make installing, removing, and searching for packages easier, and welcomes contributions from the open source community.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## About

archpkg-helper is designed for users who want an easier way to manage packages on Linux systems. While originally inspired by Arch Linux, this tool aims to work on any Linux distribution that supports Python and common package managers. Whether you’re new to Linux or a seasoned user, this tool offers simple commands for common package operations.

## Features

- Install, remove, and search for packages with simple commands
- Support for dependencies and AUR packages (coming soon)
- Easy-to-read output and error messages
- Not bound to Arch Linux—can be used on other Linux distros with compatible package managers

## Installation

You can install archpkg-helper on any Linux distro. Here are the steps:

### Prerequisites

- Python 3.6 or newer
- `git` installed

### Steps

```sh
git clone https://github.com/AdmGenSameer/archpkg-helper.git
cd archpkg-helper
pip install .
```

Or for development:

```sh
pip install -e .
```

## Usage

After installing, use the following commands:

```sh
archpkg-helper install <package-name>
archpkg-helper remove <package-name>
archpkg-helper search <package-name>
```

Replace `<package-name>` with the package you want to manage.

## File Structure

```
archpkg-helper/
│
├── archpkg_helper/        # Main Python package
│   ├── __init__.py
│   ├── cli.py             # Command-line interface implementation
│   ├── core.py            # Core logic for package management
│   └── utils.py           # Utility functions
│
├── tests/                 # Unit tests
│   ├── test_cli.py
│   └── test_core.py
│
├── setup.py               # Python packaging configuration
├── LICENSE                # Project license (Apache 2.0)
├── README.md              # This file
└── CONTRIBUTING.md        # Contribution guidelines
```

## Contributing

We welcome contributions! Please read our [`CONTRIBUTING.md`](./CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository.
2. Create a branch: `git checkout -b feature-branch`
3. Make your changes and commit: `git commit -m "Describe your changes"`
4. Push to your fork: `git push origin feature-branch`
5. Open a Pull Request.

#### Issues

Report bugs or request features [here](https://github.com/AdmGenSameer/archpkg-helper/issues).

## License

This project is licensed under the [Apache License 2.0](./LICENSE).

---

*Happy hacking!*