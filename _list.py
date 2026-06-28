import os
root = r'c:\Users\D.V.Praneeth\OneDrive\Desktop\agriguard-ai'
skip = {'.git','node_modules','venv','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','build','dist'}
files = []
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in skip]
    rel = os.path.relpath(dirpath, root)
    for f in filenames:
        files.append(os.path.join(rel, f))
for p in sorted(files):
    print(p)
