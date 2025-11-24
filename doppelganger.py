from tkinter import filedialog
from pathlib import Path
import os
import hashlib
from time import time

# add a size for which larger files will not be read
# add a file size histogram
# add command arguments
# add a .gitignore like file to ignore some common repeated files

# to ignore, anything inside:
# node_modules
# site-packages

IGNORE = [
   "node_modules", 
   "site-packages", 
   "akefile", 
   ".git" 
]

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

if os.name == 'nt':
    # OS is windows, import windows specific libraries
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)



# --- driver code ---
root = Path(filedialog.askdirectory())
print(root)

start_time = time()

files = []
for path in root.rglob("*"):
    if path.is_file() and not any(k in str(path) for k in IGNORE):
        md5 = hashlib.md5()
        with open(path, 'rb') as file:            
            while chunk := file.read(4096):
                md5.update(chunk)

        digest = md5.hexdigest()
        # print(f"{path.name}: {digest}")
        files.append((path, digest))

files.sort(key=lambda x: x[1])

last_hash = None
repeat_names = [files[0][0]]
for name, cur_hash in files:
    if cur_hash == last_hash:
        repeat_names.append(name)
    else:
        if len(repeat_names) > 1:
            print(f"\n{len(repeat_names)} repeated files ({convert_bytes(repeat_names[0].stat().st_size)} each):")
            for n in repeat_names:
                print(n.relative_to(root))
        last_hash = cur_hash
        repeat_names = [name]

input(f"\n\nSearch took {round(time()-start_time, 3)} s\nPress to exit")