import subprocess

def search_flatpak(query):
    if not query or not query.strip():
        raise ValueError("Empty search query provided")
    
    try:
        subprocess.run(['flatpak', '--version'], 
                      capture_output=True, check=True, timeout=5)
    except FileNotFoundError:
        raise FileNotFoundError("flatpak command not found. Install flatpak first.")
    except subprocess.CalledProcessError:
        raise RuntimeError("flatpak is installed but not working properly.")
    except subprocess.TimeoutExpired:
        raise TimeoutError("flatpak is not responding. Check if the service is running.")

    try:
        result = subprocess.run(
            ['flatpak', 'search', query.strip()], 
            capture_output=True, 
            text=True,
            timeout=30,
            check=False
        )
        
        if result.returncode == 1:
            return []
        elif result.returncode != 0:
            error_msg = result.stderr.strip()
            if "No remotes found" in error_msg:
                raise RuntimeError("No Flatpak remotes configured. Run: flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
            else:
                raise RuntimeError(f"flatpak search failed: {error_msg or 'Unknown error'}")

        output = result.stdout.strip()
        if not output:
            return []

        lines = output.split('\n')
        if len(lines) < 2:
            return []

        packages = []
        for line in lines[1:]:  
            if not line.strip():
                continue
            cols = line.split('\t') 
            if len(cols) >= 3:
                name = cols[0].strip()
                description = cols[1].strip()
                app_id = cols[2].strip()
                packages.append((app_id, f"{name} - {description}", 'Flatpak'))
        
        return packages
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("Flatpak search timed out. Check your internet connection.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during flatpak search: {str(e)}")