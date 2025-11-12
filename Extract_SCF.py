import re
from pathlib import Path

def extract_scf_energy(log_file):
    # Pattern to catch any SCF Done line and extract first floating number after
    pattern = re.compile(r'SCF Done.*?(-?\d+\.\d+)')
    energy = None
    with open(log_file) as f:
        for line in f:
            match = pattern.search(line)
            if match:
                energy = float(match.group(1))
    return energy

def main():
    input_dir = Path('shifted_outputs')
    output_file = Path('scf_energies.txt')
    log_files = sorted(input_dir.glob('*.log'))
    
    with output_file.open('w') as out:
        out.write("Filename\tSCF Energy (Hartree)\n")
        for logfile in log_files:
            energy = extract_scf_energy(logfile)
            if energy is not None:
                out.write(f"{logfile.name}\t{energy:.8f}\n")
            else:
                out.write(f"{logfile.name}\tNot Found\n")
    print(f"SCF energies extracted to {output_file}")

if __name__ == "__main__":
    main()
