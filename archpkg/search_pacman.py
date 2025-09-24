# search_pacman.py

import subprocess

def search_pacman(query):
    if not query or not query.strip():
        raise ValueError("Empty search query provided")

    try:
        subprocess.run(['pacman', '--version'], 
                      capture_output=True, check=True, timeout=5)
    except FileNotFoundError:
        raise FileNotFoundError("pacman command not found. This system may not be Arch-based.")
    except subprocess.CalledProcessError:
        raise RuntimeError("pacman is installed but not working properly.")
    except subprocess.TimeoutExpired:
        raise TimeoutError("pacman is not responding. The package manager may be locked or misconfigured.")
    
    try:
        result = subprocess.run(
            ['pacman', '-Ss', query.strip()],
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )

        if result.returncode == 1 and not result.stdout.strip():
            return []
        elif result.returncode != 0:
            error_msg = result.stderr.strip()
            if "could not" in error_msg.lower():
                raise RuntimeError("pacman database not initialized or corrupted. Try: sudo pacman -Syu")
            else:
                raise RuntimeError(f"pacman search failed: {error_msg or 'Unknown error'}")

        output = result.stdout.strip()
        if not output:
            return []

        lines = output.split('\n')
        results = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if "/" in line:  
                parts = line.split()
                if len(parts) >= 2:
                    pkg_full = parts[0]    
                    pkg_name = pkg_full.split("/")[-1]
                    desc = lines[i + 1].strip() if i + 1 < len(lines) else "No description"
                    results.append((pkg_name, desc, "Pacman"))
                i += 2
            else:
                i += 1

        return results

    except subprocess.TimeoutExpired:
        raise TimeoutError("pacman search timed out. The package database might be updating.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during pacman search: {str(e)}")
