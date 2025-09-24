#!/usr/bin/python
# archpkg.py

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webbrowser
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import typer
from search_aur import search_aur
from search_pacman import search_pacman
from search_flatpak import search_flatpak
from search_snap import search_snap
from search_apt import search_apt
from search_dnf import search_dnf
from command_gen import generate_command

console = Console()
app = typer.Typer(help="Universal Package Helper CLI")

try:
    import distro
except ModuleNotFoundError:
    console.print(Panel(
        "[red]❌ Required dependency 'distro' is not installed.[/red]\n\n"
        "[bold yellow]To fix this issue:[/bold yellow]\n"
        "• Run: [cyan]pip install distro[/cyan]\n"
        "• Or reinstall the package: [cyan]pip install --upgrade archpkg-helper[/cyan]\n"
        "• If using pipx: [cyan]pipx reinstall archpkg-helper[/cyan]",
        title="Missing Dependency",
        border_style="red"
    ))
    sys.exit(1)

JUNK_KEYWORDS = ["icon", "dummy", "meta", "symlink", "wrap", "material", "launcher", "unionfs"]
LOW_PRIORITY_KEYWORDS = ["extension", "plugin", "helper", "daemon", "patch", "theme"]
SUPPORTED_PLATFORMS = ["arch", "debian", "ubuntu", "linuxmint", "fedora", "manjaro"]

def detect_distro():
    """Detect the current Linux distribution with detailed error handling."""
    try:
        dist = distro.id().lower().strip()
        
        if not dist:
            console.print(Panel(
                "[yellow]⚠️ Unable to detect your Linux distribution.[/yellow]\n\n"
                "[bold cyan]Possible solutions:[/bold cyan]\n"
                "• Ensure you're running on a supported Linux distribution\n"
                "• Check if /etc/os-release file exists\n"
                "• Try running: [cyan]cat /etc/os-release[/cyan]",
                title="Distribution Detection Warning",
                border_style="yellow"
            ))
            return "unknown"

        DISTRO_MAP = {
            "arch": "arch",
            "manjaro": "arch", 
            "endeavouros": "arch",
            "arco": "arch",
            "garuda": "arch",
            "ubuntu": "debian",
            "debian": "debian", 
            "linuxmint": "debian",
            "pop": "debian",
            "elementary": "debian",
            "fedora": "fedora",
            "rhel": "fedora",
            "centos": "fedora", 
            "rocky": "fedora",
            "alma": "fedora"
        }

        detected_family = DISTRO_MAP.get(dist, "unknown")
        
        if detected_family == "unknown":
            console.print(Panel(
                f"[yellow]⚠️ Unsupported distribution detected: '{dist}'[/yellow]\n\n"
                "[bold cyan]What you can do:[/bold cyan]\n"
                "• Only Flatpak and Snap searches will be available\n"
                "• Consider requesting support for your distribution\n"
                f"• Supported distributions: {', '.join(SUPPORTED_PLATFORMS)}",
                title="Unsupported Distribution",
                border_style="yellow"
            ))
        
        return detected_family
        
    except Exception as e:
        console.print(Panel(
            f"[red]❌ Failed to detect your Linux distribution.[/red]\n\n"
            f"[bold]Error details:[/bold] {str(e)}\n\n"
            "[bold cyan]Troubleshooting steps:[/bold cyan]\n"
            "• Ensure you're running on a Linux system\n"
            "• Check if the 'distro' package is properly installed\n"
            "• Try reinstalling: [cyan]pip install --upgrade distro[/cyan]\n"
            "• Report this issue if the problem persists",
            title="Distribution Detection Failed",
            border_style="red"
        ))
        return "unknown"

def is_valid_package(name, desc):
    """Check if a package is valid (not junk/meta package)."""
    desc = (desc or "").lower()
    return not any(bad in desc for bad in JUNK_KEYWORDS)

def get_top_matches(query, all_packages, limit=5):
    """Get top matching packages with improved scoring algorithm."""
    if not all_packages:
        return []
        
    query = query.lower()
    query_tokens = set(query.split())
    scored_results = []

    for name, desc, source in all_packages:
        if not is_valid_package(name, desc):
            continue

        name_l = name.lower()
        desc_l = (desc or "").lower()
        name_tokens = set(name_l.replace("-", " ").split())
        desc_tokens = set(desc_l.split())

        score = 0

        # Exact match scoring
        if query == name_l:
            score += 150
        elif query in name_l:
            score += 80

        # 🔍 Fuzzy token matching
        for q in query_tokens:
            for token in name_tokens:
                if token.startswith(q):
                    score += 4
            for token in desc_tokens:
                if token.startswith(q):
                    score += 1

        # 💡 Boost keywords
        boost_keywords = ["editor", "browser", "ide", "official", "gui", "android", "studio", "stable", "canary", "beta"]
        for word in boost_keywords:
            if word in name_l or word in desc_l:
                score += 3

        # 🛑 Penalize junk
        for bad in LOW_PRIORITY_KEYWORDS:
            if bad in name_l or bad in desc_l:
                score -= 10

        if name_l.endswith("-bin"):
            score += 5

        # 📦 Source priority
        if source == "pacman" or source == "apt" or source == "dnf":
            score += 40
        elif source == "aur":
            score += 20
        elif source == "flatpak":
            score += 10
        elif source == "snap":
            score += 5

        scored_results.append(((name, desc, source), score))

    scored_results.sort(key=lambda x: x[1], reverse=True)
    top = [pkg for pkg, score in scored_results if score > 0][:limit]
    return top

def github_fallback(query):
    """Provide GitHub search fallback with clear messaging."""
    console.print(Panel(
        f"[yellow]🔎 No packages found for '{query}' in available repositories.[/yellow]\n\n"
        "[bold cyan]Alternative options:[/bold cyan]\n"
        "• Search GitHub for source code or releases\n"
        "• Check if the package name is spelled correctly\n" 
        "• Try searching with different keywords\n"
        "• Look for similar packages with: [cyan]archpkg <similar-name>[/cyan]",
        title="No Packages Found",
        border_style="yellow"
    ))
    
    try:
        url = f"https://github.com/search?q={query.replace(' ', '+')}&type=repositories"
        console.print(f"[blue]🌐 Opening GitHub search:[/blue] {url}")
        webbrowser.open(url)
    except Exception as e:
        console.print(Panel(
            f"[red]❌ Failed to open web browser.[/red]\n\n"
            f"[bold]Error:[/bold] {str(e)}\n\n"
            "[bold cyan]Manual search:[/bold cyan]\n"
            f"• Visit: https://github.com/search?q={query.replace(' ', '+')}&type=repositories\n"
            "• Or search manually on GitHub",
            title="Browser Error", 
            border_style="red"
        ))

def handle_search_errors(source_name, error):
    """Centralized error handling for search operations."""
    error_messages = {
        "aur": {
            "connection": "Cannot connect to AUR servers. Check your internet connection.",
            "timeout": "AUR search timed out. Try again later.",
            "generic": "AUR search failed. The service might be temporarily unavailable."
        },
        "pacman": {
            "not_found": "pacman command not found. Install pacman or run on Arch-based system.",
            "permission": "Permission denied running pacman. Check your user permissions.",
            "generic": "pacman search failed. Ensure pacman is properly installed."
        },
        "flatpak": {
            "not_found": "flatpak command not found. Install flatpak first.",
            "no_remotes": "No Flatpak remotes configured. Run: flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
            "generic": "Flatpak search failed. Ensure Flatpak is properly configured."
        },
        "snap": {
            "not_found": "snap command not found. Install snapd first.",
            "not_running": "snapd service is not running. Run: sudo systemctl start snapd",
            "generic": "Snap search failed. Ensure snapd is installed and running."
        },
        "apt": {
            "not_found": "apt-cache command not found. Run on Debian/Ubuntu-based system.",
            "update_needed": "Package cache is outdated. Run: sudo apt update",
            "generic": "APT search failed. Update package cache or check APT configuration."
        },
        "dnf": {
            "not_found": "dnf command not found. Run on Fedora/RHEL-based system.",
            "cache_error": "DNF cache error. Try: sudo dnf clean all && sudo dnf makecache",
            "generic": "DNF search failed. Check DNF configuration or try clearing cache."
        }
    }
    
    # determine specific error type
    error_str = str(error).lower()
    if "connection" in error_str or "network" in error_str:
        error_type = "connection"
    elif "timeout" in error_str:
        error_type = "timeout"
    elif "not found" in error_str or "command not found" in error_str:
        error_type = "not_found"
    elif "permission" in error_str:
        error_type = "permission"
    else:
        error_type = "generic"
    
    message = error_messages.get(source_name, {}).get(error_type, f"{source_name} search encountered an error.")
    
    console.print(f"[yellow]⚠️ {source_name.upper()}: {message}[/yellow]")

def main():
    parser = argparse.ArgumentParser(description="Universal Package Helper CLI")
    parser.add_argument('query', type=str, nargs='+', help='Name of the software to search for')
    args = parser.parse_args()
    query = ' '.join(args.query)

    if not query.strip():
        console.print(Panel(
            "[red]❌ Empty search query provided.[/red]\n\n"
            "[bold cyan]Usage:[/bold cyan]\n"
            "• [cyan]archpkg firefox[/cyan] - Search for Firefox\n"
            "• [cyan]archpkg visual studio code[/cyan] - Search for VS Code\n"
            "• [cyan]archpkg --help[/cyan] - Show help information",
            title="Invalid Input",
            border_style="red"
        ))
        return

    detected = detect_distro()
    console.print(f"\n:mag: [bold green]Searching for[/bold green] '{query}' on [cyan]{detected}[/cyan] platform...\n")

    results = []
    search_errors = []

    # search based on detected distribution
    if detected == "arch":
        try:
            aur_results = search_aur(query)
            results.extend(aur_results)
        except Exception as e:
            handle_search_errors("aur", e)
            search_errors.append("AUR")
            
        try:
            pacman_results = search_pacman(query) 
            results.extend(pacman_results)
        except Exception as e:
            handle_search_errors("pacman", e)
            search_errors.append("Pacman")
            
    elif detected == "debian":
        try:
            apt_results = search_apt(query)
            results.extend(apt_results)
        except Exception as e:
            handle_search_errors("apt", e)
            search_errors.append("APT")
            
    elif detected == "fedora":
        try:
            dnf_results = search_dnf(query)
            results.extend(dnf_results)
        except Exception as e:
            handle_search_errors("dnf", e)
            search_errors.append("DNF")

    # universal package managers
    try:
        flatpak_results = search_flatpak(query)
        results.extend(flatpak_results)
    except Exception as e:
        handle_search_errors("flatpak", e)
        search_errors.append("Flatpak")

    try:
        snap_results = search_snap(query)
        results.extend(snap_results)
    except Exception as e:
        handle_search_errors("snap", e)
        search_errors.append("Snap")

    # show search summary
    if search_errors:
        console.print(f"[dim]Note: Some sources unavailable: {', '.join(search_errors)}[/dim]\n")

    if not results:
        github_fallback(query)
        return

    top_matches = get_top_matches(query, results, limit=5)
    if not top_matches:
        console.print(Panel(
            f"[yellow]⚠️ Found {len(results)} packages, but none match '{query}' closely.[/yellow]\n\n"
            "[bold cyan]Suggestions:[/bold cyan]\n"
            "• Try a more specific search term\n"
            "• Check spelling of the package name\n"
            "• Use broader keywords (e.g., 'editor' instead of 'vim')\n"
            f"• Search GitHub: [cyan]https://github.com/search?q={query.replace(' ', '+')}[/cyan]",
            title="No Close Matches",
            border_style="yellow"
        ))
        return

    table = Table(title="Top Matching Packages")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Package Name", style="green")
    table.add_column("Source", style="blue")
    table.add_column("Description", style="magenta")

    for idx, (pkg, desc, source) in enumerate(top_matches, 1):
        table.add_row(str(idx), pkg, source, desc or "No description")

    console.print(table)

    try:
        choice = input("\nSelect a package to install [1-5 or press Enter to cancel]: ")
        if not choice.strip():
            console.print("[yellow]⚠️ Installation cancelled by user.[/yellow]")
            return
            
        try:
            choice = int(choice)
        except ValueError:
            console.print(Panel(
                "[red]❌ Invalid input. Please enter a number.[/red]\n\n"
                "[bold cyan]Valid options:[/bold cyan]\n"
                "• Enter 1-5 to select a package\n"
                "• Press Enter to cancel\n"
                "• Use Ctrl+C to exit",
                title="Invalid Input",
                border_style="red"
            ))
            return
            
        if not (1 <= choice <= len(top_matches)):
            console.print(Panel(
                f"[red]❌ Choice {choice} is out of range.[/red]\n\n"
                f"[bold cyan]Available options:[/bold cyan] 1-{len(top_matches)}\n"
                "• Try again with a valid number\n"
                "• Press Enter to cancel",
                title="Invalid Choice",
                border_style="red"
            ))
            return
            
        selected_pkg = top_matches[choice - 1]
        pkg, desc, source = selected_pkg
        command = generate_command(pkg, source)
        
        if not command:
            console.print(Panel(
                f"[red]❌ Cannot generate install command for {source} packages.[/red]\n\n"
                "[bold cyan]Possible solutions:[/bold cyan]\n"
                f"• Install {source.lower()} package manager first\n"
                "• Check if the package manager is in your PATH\n"
                f"• Manually install: check {source.lower()} documentation",
                title="Command Generation Failed",
                border_style="red"
            ))
            return
            
        console.print(f"\n[bold green]✅ Install Command:[/bold green] {command}")
        console.print("[bold yellow]Press Enter to install, or Ctrl+C to cancel...[/bold yellow]")
        
        try:
            input()
            console.print("[blue]⏳ Running install command...[/blue]")
            exit_code = os.system(command)
            
            if exit_code != 0:
                console.print(Panel(
                    f"[red]❌ Installation failed with exit code {exit_code}.[/red]\n\n"
                    "[bold cyan]Troubleshooting:[/bold cyan]\n"
                    "• Check if you have sufficient permissions\n"
                    "• Ensure package manager is properly configured\n"
                    "• Try running the command manually\n"
                    f"• Command: [cyan]{command}[/cyan]",
                    title="Installation Failed",
                    border_style="red"
                ))
            else:
                console.print(f"[bold green]✅ Successfully installed {pkg}![/bold green]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ Installation cancelled by user.[/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Selection cancelled by user.[/yellow]")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Operation cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(Panel(
            f"[red]❌ An unexpected error occurred.[/red]\n\n"
            f"[bold]Error details:[/bold] {str(e)}\n\n"
            "[bold cyan]What to do:[/bold cyan]\n"
            "• Try running the command again\n"
            "• Check if all dependencies are installed\n"
            "• Report this issue if it persists\n"
            f"• Include this error message in your report",
            title="Unexpected Error",
            border_style="red"
        ))
        sys.exit(1)

# add Typer app command to match entry point in pyproject.toml
@app.callback()
def callback():
    """Universal Package Helper CLI"""
    pass

@app.command()
def search(query: str = typer.Argument(..., help="Name of the software to search for")):
    """Search for packages across multiple sources"""
    try:
        # convert query to list format expected by main
        args = query.split()
        sys.argv = [sys.argv[0]] + args
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Search cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(Panel(
            f"[red]❌ Search operation failed.[/red]\n\n"
            f"[bold]Error details:[/bold] {str(e)}\n\n"
            "[bold cyan]Try:[/bold cyan]\n"
            "• Check your search query spelling\n"
            "• Ensure you have internet connectivity\n"
            "• Verify package managers are installed\n"
            f"• Report this error if it continues",
            title="Search Failed",
            border_style="red"
        ))
        sys.exit(1)