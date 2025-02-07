import os
import re
import pkg_resources
import sys
from pathlib import Path
from importlib.util import find_spec

STANDARD_LIBRARIES = set(sys.builtin_module_names)

def is_standard_lib(package_name):
    return package_name in STANDARD_LIBRARIES and find_spec(package_name) is not None

def find_imports_in_file(filepath):
    imports = set()
    with open(filepath, 'r') as f:
        for line in f:
            match = re.match(r'^\s*(?:import|from)\s+([\w\d_]+)', line)
            if match:
                imports.add(match.group(1))
    return imports

def get_installed_version(package_name):
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

def get_requirements(directory='.', filename='requirements.txt'):
    all_imports = set()
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                all_imports.update(find_imports_in_file(filepath))
    
    print(all_imports)
    print(STANDARD_LIBRARIES)
    for pkg in all_imports:
        print(f"{pkg}:",is_standard_lib(pkg))
    requirements = {pkg for pkg in all_imports if not is_standard_lib(pkg)}
    print(requirements)
    
    with open(filename, 'w') as req_file:
        for package in sorted(requirements):
            version = get_installed_version(package)
            if version:
                req_file.write(f"{package}=={version}\n")
            else:
                print(f"Warning: Package '{package}' not found in the environment.")
    
    print(f"'{filename}' has been generated with detected packages.")

if __name__ == "__main__":
    get_requirements()
