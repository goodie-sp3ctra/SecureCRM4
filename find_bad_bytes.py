import os

for dirpath, _, filenames in os.walk("."):
    for fn in filenames:
        if fn.endswith(".py"):
            path = os.path.join(dirpath, fn)
            with open(path, "rb") as f:
                data = f.read()
            if b"\x97" in data:
                print("Found 0x97 in", path)
