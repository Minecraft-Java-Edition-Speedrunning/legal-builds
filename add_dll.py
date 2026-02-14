import csv
import hashlib
import pathlib
import sys

output = "legal-dlls.csv"


with open(output, "r") as f:
    reader = csv.reader(f)
    fields = next(reader)
    curr = list(reader)

assert len(sys.argv) == 3
filename = sys.argv[1]
version = sys.argv[2]
file = pathlib.Path(filename)
if not file.exists():
    print(f"{file}: file does not exist!", file=sys.stderr)
    exit(1)


with open(file, "rb") as f:
    name = file.name
    checksum = hashlib.sha512(f.read()).hexdigest()
    print(f"adding {name}: {checksum}")
    curr.append([name, version, checksum])


with open(output, "w", newline="") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(fields)
    writer.writerows(curr)
