import sys
import re
from pathlib import Path

def extract_full_fragment_coords(logfile, outfile):
    atom_line_pattern = re.compile(r'^([A-Za-z]+)\(Fragment=\d+\)\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)')
    atoms = []
    recording = False
    with open(logfile) as f:
        for line in f:
            match = atom_line_pattern.match(line.strip())
            if match:
                atoms.append((
                    match.group(1),
                    float(match.group(2)),
                    float(match.group(3)),
                    float(match.group(4))
                ))
    if not atoms:
        print(f"No coordinates found in {logfile}")
        return False
    
    with open(outfile, 'w') as f_out:
        f_out.write(f"{len(atoms)}\n")
        f_out.write("Full extracted fragment coordinates\n")
        for atom, x, y, z in atoms:
            f_out.write(f"{atom} {x:.6f} {y:.6f} {z:.6f}\n")
    return True


def main():
    input_dir = Path('shifted_outputs')
    output_dir = Path('xyz_frames')
    output_dir.mkdir(exist_ok=True)
    
    log_files = sorted(input_dir.glob('*.log'))
    if not log_files:
        print(f"No .log files found in {input_dir}")
        sys.exit(1)

    # Extract xyz files
    for log_file in log_files:
        xyz_file = output_dir / f"{log_file.stem}.xyz"
        print(f"Processing {log_file} -> {xyz_file}")
        success = extract_full_fragment_coords(log_file, xyz_file)
        if not success:
            print(f"Skipping {log_file}: no coordinates found")

    # Concatenate all xyz files sorted into scan_movie.xyz
    movie_file = Path('scan_movie.xyz')
    with movie_file.open('w') as movie:
        for xyz_file in sorted(output_dir.glob('*.xyz')):
            with xyz_file.open() as f:
                # Copy all lines
                contents = f.read()
                movie.write(contents)
    
    print(f"Created movie file {movie_file}")

if __name__ == "__main__":
    main()
