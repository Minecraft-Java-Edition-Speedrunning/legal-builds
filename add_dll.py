import argparse
import csv
import hashlib
import pathlib
import sys

output = pathlib.Path("legal-dlls.csv")

with open(output, "r") as f:
    reader = csv.reader(f)
    fields = next(reader)
    curr = list(reader)

parser = argparse.ArgumentParser("add dll")
parser.add_argument("file", type=pathlib.Path)
parser.add_argument("version")
args = parser.parse_args()
file = args.file
if not file.exists():
    print(f"{file}: file does not exist!", file=sys.stderr)
    exit(1)

name = file.name
checksum = hashlib.sha512(file.read_bytes()).hexdigest()
print(f"adding {name}: {checksum}")
curr.append([name, args.version, checksum])

with open(output, "w", newline="") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(fields)
    writer.writerows(curr)
