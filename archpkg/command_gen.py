from typing import Tuple

def generate_command(pkg_name: str, source: str) -> Tuple[str, str]:
    
    if source == 'Pacman':
        return (
            f"sudo pacman -S {pkg_name}",
            "Requires: pacman (Arch package manager), sudo access"
        )
    elif source == 'AUR':
        return (
            f"yay -S {pkg_name}",
            "Requires: yay (AUR helper). Install with 'pacman -S yay' first if needed."
        )
    elif source == 'Flatpak':
        return (
            f"flatpak install flathub {pkg_name}",
            "Requires: flatpak. Install with 'pacman -S flatpak' first if needed."
        )
    else:
        raise ValueError(f"Unknown package source: {source}")


import subprocess

def check_command_availability(command):
    # check if a command is available in the system PATH
    try:
        subprocess.run([command, '--version'], 
                      capture_output=True, 
                      check=True, 
                      timeout=5)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def generate_command(pkg_name, source):
    if not pkg_name or not pkg_name.strip():
        raise ValueError("Package name cannot be empty")
        
    if not source or not source.strip():
        raise ValueError("Package source cannot be empty")
        
    pkg_name = pkg_name.strip()
    source = source.strip().lower()
    
    # it will generate commands based on source
    if source == 'pacman':
        if not check_command_availability('pacman'):
            raise RuntimeError("pacman is not installed or not available in PATH. Install pacman or run on an Arch-based system.")
        return f"sudo pacman -S {pkg_name}"
        
    elif source == 'aur':
        # check for common AUR helpers in order of preference
        aur_helpers = ['yay', 'paru', 'trizen', 'yaourt']
        available_helper = None
        
        for helper in aur_helpers:
            if check_command_availability(helper):
                available_helper = helper
                break
                
        if not available_helper:
            raise RuntimeError(
                "No AUR helper found. Install one of the following:\n"
                "• yay: sudo pacman -S yay\n"
                "• paru: sudo pacman -S paru\n"
                "• Or build manually from AUR"
            )
        return f"{available_helper} -S {pkg_name}"
        
    elif source == 'flatpak':
        if not check_command_availability('flatpak'):
            raise RuntimeError("Flatpak is not installed. Install it with your system package manager.")
        return f"flatpak install flathub {pkg_name}"
        
    elif source == 'apt':
        if not check_command_availability('apt'):
            raise RuntimeError("APT is not available. This command requires a Debian/Ubuntu-based system.")
        return f"sudo apt install {pkg_name}"
        
    elif source == 'dnf':
        if not check_command_availability('dnf'):
            raise RuntimeError("DNF is not available. This command requires a Fedora/RHEL-based system.")
        return f"sudo dnf install {pkg_name}"
        
    elif source == 'snap':
        if not check_command_availability('snap'):
            raise RuntimeError("Snap is not installed. Install snapd with your system package manager.")
        return f"sudo snap install {pkg_name}"
        
    else:
        raise ValueError(
            f"Unsupported package source: '{source}'. "
            "Supported sources: pacman, aur, flatpak, apt, dnf, snap"
        )

def get_install_suggestions(source):
    suggestions = {
        'pacman': [
            "This package requires an Arch-based Linux distribution",
            "Consider using the Flatpak or Snap version if available"
        ],
        'aur': [
            "Install an AUR helper like yay: sudo pacman -S yay",
            "Or manually build from AUR following the Arch Wiki"
        ],
        'flatpak': [
            "Install Flatpak:",
            "• Arch: sudo pacman -S flatpak",
            "• Ubuntu: sudo apt install flatpak",
            "• Fedora: sudo dnf install flatpak"
        ],
        'apt': [
            "This package requires a Debian/Ubuntu-based system",
            "Consider using the Flatpak or Snap version if available"
        ],
        'dnf': [
            "This package requires a Fedora/RHEL-based system", 
            "Consider using the Flatpak or Snap version if available"
        ],
        'snap': [
            "Install Snap:",
            "• Arch: sudo pacman -S snapd && sudo systemctl enable --now snapd",
            "• Ubuntu: sudo apt install snapd",
            "• Fedora: sudo dnf install snapd"
        ]
    }
    
    return suggestions.get(source.lower(), ["Check your system's package manager documentation"])

def validate_package_name(pkg_name):
    if not pkg_name:
        return False, "Package name cannot be empty"
        
    # basic validation for invalid characters
    invalid_chars = ['/', '\\', '<', '>', '|', '&', ';', '`', '$']
    for char in invalid_chars:
        if char in pkg_name:
            return False, f"Package name contains invalid character: '{char}'"

    if len(pkg_name) > 100:
        return False, "Package name is too long"
        
    return True, "Valid package name"
