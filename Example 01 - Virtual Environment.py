# Example 01 - Virtual Environment
# Every project should get its own set of installed packages, so that projects do not
# break each other (and your system Python). That is what a virtual environment (venv) is.
#
# Create and activate one, in the project folder:
#   python -m venv .venv
#   .venv\Scripts\activate               (Windows)
#   source .venv/bin/activate            (Linux / Raspberry Pi)
# Install the packages of this project, and leave the venv when done:
#   pip install -r requirements.txt
#   deactivate
#
# Run this script once BEFORE and once AFTER activating the venv, and compare the output.
# (On a recent Raspberry Pi OS, pip refuses to install outside a venv - this is why.)
#
# Concepts: venv, pip, requirements.txt, sys.prefix, importlib.metadata

import sys
from importlib import metadata

# Inside a venv, sys.prefix points to the venv folder, sys.base_prefix to the real Python
in_venv = sys.prefix != sys.base_prefix

print("Python executable :", sys.executable)
print("Python version    :", sys.version.split()[0])
print("Inside a venv     :", "YES" if in_venv else "NO")
if in_venv:
    print("venv folder       :", sys.prefix)
else:
    print("Tip: create a venv first (see the top of this file)")

print()
print("Packages needed by the examples:")
for package in ["pandas", "numpy", "matplotlib", "pymysql", "streamlit", "guizero"]:
    try:
        print(f"  {package:<12} {metadata.version(package)}")
    except metadata.PackageNotFoundError:
        print(f"  {package:<12} not installed  ->  pip install {package}")
