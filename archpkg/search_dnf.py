# search_dnf.py

import subprocess

def search_dnf(query):
    if not query or not query.strip():
        raise ValueError("Empty search query provided")
    
    try:
        subprocess.run(['dnf', '--version'], 
                      capture_output=True, check=True, timeout=5)
    except FileNotFoundError:
        raise FileNotFoundError("dnf command not found. This system may not be Fedora/RHEL-based.")
    except subprocess.CalledProcessError:
        raise RuntimeError("dnf is installed but not working properly.")
    except subprocess.TimeoutExpired:
        raise TimeoutError("dnf is not responding.")

    try:
        result = subprocess.run(
            ["dnf", "search", query.strip()], 
            capture_output=True, 
            text=True,
            timeout=60,  # DNF can be slower
            check=False
        )
        
        if result.returncode == 1:  # no matches found
            return []
        elif result.returncode != 0:
            error_msg = result.stderr.strip()
            if "Error: Cache disabled" in error_msg:
                raise RuntimeError("DNF cache is disabled. Try: sudo dnf makecache")
            elif "Cannot retrieve metalink" in error_msg:
                raise ConnectionError("Cannot connect to DNF repositories. Check internet connection.")
            elif "Permission denied" in error_msg:
                raise PermissionError("Permission denied accessing DNF. Try: sudo dnf search")
            else:
                raise RuntimeError(f"dnf search failed: {error_msg or 'Unknown error'}")

        output = result.stdout.strip()
        if not output:
            return []

        packages = []
        in_results = False
        
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if "====" in line or "Name" in line and "Matched" in line:
                in_results = True
                continue
                
            if in_results and line and not line.startswith("Last metadata"):
                if " : " in line:
                    parts = line.split(" : ", 1)
                    if len(parts) == 2:
                        name_version = parts[0].strip()
                        desc = parts[1].strip()
                        name = name_version.split('.')[0]
                        packages.append((name, desc, "DNF"))
                        
        return packages
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("DNF search timed out. This can happen with large repositories.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during DNF search: {str(e)}")        
