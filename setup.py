from setuptools import setup, find_packages

setup(
    name='archpkg-helper',
    version='0.1.0',
    packages=find_packages(),  # Automatically finds the archpkg/ folder
    install_requires=[
        'requests',
        'rich',
        'fuzzywuzzy',
        'python-Levenshtein',
        'distro',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'archpkg = archpkg.cli:main'  # entry point: archpkg/cli.py -> main()
        ]
    },
    author='AdmGenSameer',
    description='Cross-distro CLI to search and generate install commands for packages (pacman, AUR, apt, dnf, flatpak, snap).',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Software Distribution'
    ],
    python_requires='>=3.7'
)
