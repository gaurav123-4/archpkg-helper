from setuptools import setup

setup(
    name='archpkg-helper',
    version='0.1.0',
    py_modules=['archpkg', 'search_aur', 'search_pacman', 'search_flatpak', 'command_gen'],
    install_requires=[
        'requests',
        'rich',
        'fuzzywuzzy',
        'python-Levenshtein'  # Required for fuzzywuzzy speed
    ],
    entry_points={
        'console_scripts': [
            'archpkg = archpkg:main'
        ]
    },
    author='AdmGenSameer',
    description='A CLI tool to search and generate install commands for Arch Linux packages (pacman, AUR, flatpak).',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
    ],
)
