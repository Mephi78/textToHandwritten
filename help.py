from maincode import getname, arr
import os

missing = []
for ch in arr:
    name = getname(ch)
    if not os.path.exists(f"myfont/{name}.png"):
        missing.append(f"{name}.png")

print("Missing character images:")
for file in missing:
    print(file)
