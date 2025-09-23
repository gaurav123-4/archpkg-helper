def generate_command(pkg_name, source):
    if source == 'Pacman':
        return f"sudo pacman -S {pkg_name}"
    elif source == 'AUR':
        return f"yay -S {pkg_name}"
    elif source == 'Flatpak':
        return f"flatpak install flathub {pkg_name}"
    elif source == 'APT':
        return f"sudo apt install {pkg_name}"
    elif source == 'DNF':
        return f"sudo dnf install {pkg_name}"
    elif source == 'Snap':
        return f"sudo snap install {pkg_name}"
    return ""
