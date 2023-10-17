import os

output = []
files = ['shims', 'utils', 'mapping', 'mutablemapping', 'chainmap', 'template']

for fname in files:
    with open(f"../template/{fname}.py", "r", encoding='utf-8') as f:
        output.append(f"==== {fname}.py =====")
        for line in f.readlines():
            if not(line.startswith("import") or line.startswith("from")):
                output.append(line)
        output.append("\n\n")

with open("../dist/combined.py", "w", encoding='utf-8') as f:
    f.write("\n".join(output))
    