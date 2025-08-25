from pathlib import Path
import argparse
from tqdm import tqdm

def rm_tree(pth: Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


parser = argparse.ArgumentParser(
                    prog="organiser.py",
                    description="Organise files downloaded from NCBI datasets"
                    )
parser.add_argument("indir", help="Input directory (after unzip)")
parser.add_argument("outdir", help="Name of output directory")
args = parser.parse_args()

indir = Path(args.indir)
outdir = Path(args.outdir)
data_dir = indir / "data"

if not data_dir.exists():
    raise FileNotFoundError("Input directory doesn't contain 'data' subdirectory")

subdirs = [subdir for subdir in data_dir.glob("*") if subdir.is_dir()]

# Create output directories and organize
outdir.mkdir(exist_ok=True)
file_types = ["protein", "genomic"]
for subdir in tqdm(subdirs, desc="Organizing files"):
    input_files = subdir.glob("*")
    assembly = subdir.stem
    for f in input_files:
        for file_type in file_types:
            if file_type not in f.stem:
                continue
            file_type_dir = outdir / file_type
            file_type_dir.mkdir(exist_ok=True)
            new_name = assembly + f.suffix
            f.rename(file_type_dir / new_name)

# Remove input directory
rm_tree(indir)
readme_file = outdir / "README.md"
readme_file.unlink()
