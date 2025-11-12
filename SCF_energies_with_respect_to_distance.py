import re
from pathlib import Path

def extract_scf_energy(log_file):
    pattern = re.compile(r'SCF Done:\s+E\([RU]?[\w\d-]+\)\s+=\s+(-?\d+\.\d+)')
    energy = None
    with open(log_file) as f:
        for line in f:
            match = pattern.search(line)
            if match:
                energy = float(match.group(1))
    return energy

def main():
    input_dir = Path('shifted_outputs')
    output_file = Path('scf_energies_dist.txt')
    log_files = sorted(input_dir.glob('*.log'))

    start_distance = 0.0  # Starting distance in Angstroms
    increment = 0.1       # Distance increment per step

    with output_file.open('w') as out:
        out.write("Distance(Angstrom)\tSCF Energy (Hartree)\n")
        for i, logfile in enumerate(log_files):
            energy = extract_scf_energy(logfile)
            dist = start_distance + i*increment
            if energy is not None:
                out.write(f"{dist:.4f}\t{energy:.8f}\n")
            else:
                out.write(f"{dist:.4f}\tNot Found\n")

    print(f"SCF energies with distances written to {output_file}")

if __name__ == "__main__":
    main()
