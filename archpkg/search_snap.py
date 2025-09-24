import subprocess

def search_snap(query):
    if not query or not query.strip():
        raise ValueError("Empty search query provided")
    
    try:
        subprocess.run(['snap', '--version'], 
                      capture_output=True, check=True, timeout=5)
    except FileNotFoundError:
        raise FileNotFoundError("snap command not found. Install snapd first.")
    except subprocess.CalledProcessError as e:
        if "system does not fully support snapd" in e.stderr:
            raise RuntimeError("This system does not support snap packages.")
        else:
            raise RuntimeError("snapd is installed but not working properly.")
    except subprocess.TimeoutExpired:
        raise TimeoutError("snap is not responding. Check if snapd service is running.")

    try:
        result = subprocess.run(
            ["snap", "find", query.strip()], 
            capture_output=True, 
            text=True, 
            timeout=30,
            check=False
        )
        
        if result.returncode == 1: 
            return []
        elif result.returncode != 0:
            error_msg = result.stderr.strip()
            if "cannot communicate with server" in error_msg:
                raise ConnectionError("Cannot connect to Snap Store. Check internet connection.")
            else:
                raise RuntimeError(f"snap search failed: {error_msg or 'Unknown error'}")

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
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                desc = " ".join(parts[1:])[:100] + ("..." if len(" ".join(parts[1:])) > 100 else "")
                packages.append((name, desc, "Snap"))
        
        return packages
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("Snap search timed out. Check your internet connection.")
    except ConnectionError:
        raise ConnectionError("Cannot connect to Snap Store servers.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during snap search: {str(e)}")