import os
import re
from pathlib import Path

# User Settings
input_file = 'input.gjf'            # Original Gaussian input file
axis = 'y'                          # Axis to shift ('x', 'y', or 'z')
step = 0.1                          # Increment per step (Angstrom)
n_steps = 30                        # Number of increments
total_shift = step * n_steps        # Total shift
fragment_to_shift = 1               # Fragment number to shift (e.g. 1 or 2)
output_dir = Path('shifted_outputs')
output_dir.mkdir(exist_ok=True)

axis_dict = {'x': 0, 'y': 1, 'z': 2}
if axis.lower() not in axis_dict:
    raise ValueError("Axis must be 'x', 'y', or 'z'")
coord_idx = axis_dict[axis.lower()]

with open(input_file, 'r') as f:
    lines = f.readlines()

# Find coordinates section (between charge/multiplicity and next blank line)
coord_start = None
coord_end = None
fragment_re = re.compile(r'Fragment=(\d+)')
for i, line in enumerate(lines):
    if coord_start is None and re.match(r'\s*[A-Za-z]+\(Fragment=\d+\)', line):
        coord_start = i
    elif coord_start is not None and line.strip() == '':
        coord_end = i
        break
if coord_start is None or coord_end is None:
    raise RuntimeError('Could not identify coordinate section.')

fixed_head = lines[:coord_start]
coords = lines[coord_start:coord_end]
fixed_tail = lines[coord_end:]

for n in range(n_steps):
    delta = (n + 1) * step
    new_coords = []
    for cline in coords:
        parts = cline.strip().split()
        if len(parts) < 4:
            new_coords.append(cline)
            continue
        frag_match = fragment_re.search(cline)
        if not frag_match:
            new_coords.append(cline)
            continue
        frag_num = int(frag_match.group(1))
        try:
            x, y, z = map(float, parts[1:4])
        except ValueError:
            new_coords.append(cline)
            continue
        # Shift only the chosen fragment
        if frag_num == fragment_to_shift:
            coords_list = [x, y, z]
            coords_list[coord_idx] += delta
            newline = f"{parts[0]}{' ' * (15 - len(parts[0]))}{coords_list[0]:.8f}    {coords_list[1]:.8f}    {coords_list[2]:.8f}\n"
        else:
            newline = cline
        new_coords.append(newline)
    # Save to output directory
    outname = output_dir / f"shifted_frag{fragment_to_shift}_{axis}_{n+1:02d}.gjf"
    with open(outname, 'w') as fout:
        fout.writelines(fixed_head)
        fout.writelines(new_coords)
        fout.writelines(fixed_tail)
print(f"Done! {n_steps} files are saved in '{output_dir.name}' (one per step). You can download the whole folder easily.")
