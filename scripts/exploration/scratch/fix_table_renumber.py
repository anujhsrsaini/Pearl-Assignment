import re

with open(r"D:\Anuj\Pearl-ASsignment\README.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_table = False
table_num = 1

for line in lines:
    if line.startswith('| # |'):
        in_table = True
        new_lines.append(line)
        continue
    if in_table and line.startswith('|---'):
        new_lines.append(line)
        continue
    if in_table and line.startswith('|'):
        m = re.match(r'^\|\s*\d+\s*\|\s*(.*)$', line)
        if m:
            new_lines.append(f"| {table_num} | {m.group(1)}\n")
            table_num += 1
            continue
        else:
            in_table = False
    new_lines.append(line)

with open(r"D:\Anuj\Pearl-ASsignment\README.md", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Renumbered table to {table_num - 1} columns!")
