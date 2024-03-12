import sys

'''
grep alloc_total libleak.3946648 | tee 1
alloc_total 22955482 + 513 0x55e4a83103b0
alloc_total 22955521 + 39 0x55e4a831a7e0
alloc_total 22955560 + 39 0x55e4a88d1730
alloc_total 22956064 + 504 0x55e4a7fea490
alloc_total 22964256 + 8192 0x55e4a87dca40
alloc_total 22956142 U 8192 78 0x55e4a87dca40
alloc_total 22955638 - 504 0x55e4a7fea490
alloc_total 22955560 - 78 0x55e4a87dca40
alloc_total 22955521 - 39 0x55e4a88d1730
alloc_total 22955482 - 39 0x55e4a831a7e0
alloc_total 22954969 - 513 0x55e4a83103b0
alloc_total 22955482 + 513 0x55e4a83103b0
alloc_total 22954969 - 513 0x55e4a83103b0
alloc_total 22955482 + 513 0x55e4a83103b0
alloc_total 22958385 + 2903 0x55e4a87c76a0
alloc_total 22959410 + 1025 0x55e4a7f5c8c0
alloc_total 22958897 - 513 0x55e4a83103b0
alloc_total 22960946 + 2049 0x55e4a84da430
alloc_total 22959921 - 1025 0x55e4a7f5c8c0
alloc_total 22964018 + 4097 0x55e4a850fb40
alloc_total 22961969 - 2049 0x55e4a84da430
alloc_total 22959066 - 2903 0x55e4a87c76a0
alloc_total 22954969 - 4097 0x55e4a850fb40
alloc_total 22959065 + 4096 0x55e4a850fb40
alloc_total 22954969 - 4096 0x55e4a850fb40

python3 check_libleak.py 1
'''

def group_lines_by_last_column(lines):
    grouped_lines = {}
    for line in lines:
        columns = line.split()
        key = columns[-1]
        if key not in grouped_lines:
            grouped_lines[key] = []
        grouped_lines[key].append(line)
    return grouped_lines

# Function to check if each group meets the condition
def check_group_condition(group):
    length = len(group)
    i = 0
    alloc_size = 0
    while i < length:
        items = group[i].split()
        if i == 0 and items[2] == '-':
            i += 1
            continue
        elif i == length - 1 and items[2] == '+':
            break
        else:
            i += 1
            if items[2] == '+':
                if alloc_size == 0:
                    alloc_size = items[3]
                else:
                    return False
            elif items[2] == '-':
                if alloc_size == items[3]:
                    alloc_size = 0
                else:
                    return False
            elif items[2] == 'U':
                if alloc_size == items[3]:
                    alloc_size = items[4]
                else:
                    return False
            else:
                continue
    return True


# Read input text sample
with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

grouped_lines = group_lines_by_last_column(lines)

# Check condition for each group and print lines that do not meet the condition
for key, group in grouped_lines.items():
    if not check_group_condition(group):
        print(f"{key} does not meet the condition:")
        for line in group:
            print(line.strip())
        print()

