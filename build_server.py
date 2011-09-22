import sys
sys.path.append("..")
from distutils.core import setup
import py2exe
import py_compile
excludes = ["Secur32.dll", "SHFOLDER.dll"]

run = lambda: \
setup(
    options = {
        "py2exe": {
            "compressed": 1,
            "optimize": 2,
            "ascii": 1,
            "bundle_files": 1,
            "dll_excludes": excludes,
            "packages": ["encodings", "core", "email", "numpy"],
            "dist_dir": "dist",
            }
        },
    zipfile = None,
    console=[{
        'script': "server/server.py",
      #  "icon_resources": [(1, 'skype.ico')]
    }]
    )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv[1:] = ['py2exe']
    run()