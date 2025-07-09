import subprocess

def search_pacman(query):
    try:
        result = subprocess.run(['pacman', '-Ss', query], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = result.stdout.decode().strip().split('\n')

        packages = []
        for i in range(0, len(output), 2):
            if i + 1 < len(output):
                line1 = output[i]
                line2 = output[i + 1]
                parts = line1.split()
                if len(parts) >= 2:
                    name = parts[1]
                    desc = line2.strip()
                    packages.append((name, desc, 'Pacman'))
        return packages
    except Exception as e:
        return []
