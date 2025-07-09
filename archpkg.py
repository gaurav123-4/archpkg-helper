# archpkg.py

import argparse
from rich.console import Console
from rich.table import Table
from fuzzywuzzy import process
from search_aur import search_aur
from search_pacman import search_pacman
from search_flatpak import search_flatpak
from command_gen import generate_command

console = Console()

def get_best_match(query, all_packages):
    names = [pkg[0] for pkg in all_packages]
    match, _ = process.extractOne(query, names)
    for pkg in all_packages:
        if pkg[0] == match:
            return pkg
    return None

def main():
    parser = argparse.ArgumentParser(description="Arch Package Helper CLI")
    parser.add_argument('query', type=str, nargs='+', help='Name of the software to search for')
    args = parser.parse_args()
    query = ' '.join(args.query)

    console.print(f"\n:mag: [bold green]Searching for[/bold green] '{query}'...\n")

    aur_results = search_aur(query)
    pacman_results = search_pacman(query)
    flatpak_results = search_flatpak(query)

    all_results = aur_results + pacman_results + flatpak_results

    if not all_results:
        console.print("[red]❌ No packages found.[/red]")
        return

    best = get_best_match(query, all_results)

    if best:
        pkg, desc, source = best
        command = generate_command(pkg, source)

        table = Table(title="Best Match")
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        table.add_row("Package Name", pkg)
        table.add_row("Source", source)
        table.add_row("Description", desc)
        table.add_row("Install Command", command)
        console.print(table)
    else:
        console.print("[yellow]⚠️ Couldn't find a matching package.[/yellow]")

if __name__ == '__main__':
    main()
