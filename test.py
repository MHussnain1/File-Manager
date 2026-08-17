from pathlib import Path

current = Path.cwd()
print(f"current path is '{current}'")

for item in current.iterdir():
    if item.is_file():
        print("File: ",item.name)
    elif item.is_dir():
        print("DIR: ",item.name)