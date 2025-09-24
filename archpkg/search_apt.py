import subprocess

def search_apt(query):
    if not query or not query.strip():
        raise ValueError("Empty search query provided")
    
    # check if apt cache is available
    try:
        subprocess.run(['apt-cache', '--version'], 
                      capture_output=True, check=True, timeout=5)
    except FileNotFoundError:
        raise FileNotFoundError("apt-cache command not found. This system may not be Debian/Ubuntu-based.")
    except subprocess.CalledProcessError:
        raise RuntimeError("apt-cache is installed but not working properly.")
    except subprocess.TimeoutExpired:
        raise TimeoutError("apt-cache is not responding.")

    try:
        result = subprocess.run(
            ["apt-cache", "search", query.strip()], 
            capture_output=True, 
            text=True,
            timeout=30,
            check=False
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip()
            if "Unable to locate package" in error_msg:
                return []  # no packages found, which is normal
            elif "E: Could not open lock file" in error_msg:
                raise PermissionError("Cannot access APT cache. Try running: sudo apt update")
            else:
                raise RuntimeError(f"apt-cache search failed: {error_msg or 'Unknown error'}")

        output = result.stdout.strip()
        if not output:
            return []

        packages = []
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            if ' - ' in line:
                name, desc = line.split(' - ', 1)
                packages.append((name.strip(), desc.strip(), "APT"))
            
        return packages
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("APT search timed out. Try updating package cache: sudo apt update")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during APT search: {str(e)}")