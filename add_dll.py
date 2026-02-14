import csv
import hashlib
import pathlib
import sys

output = "legal-dlls.csv"


with open(output, "r") as f:
    reader = csv.reader(f)
    fields = next(reader)
    curr = list(reader)


for filename in sys.argv[1:]:
    file = pathlib.Path(filename)
    if not file.exists():
        print(f"{file}: file does not exist!", file=sys.stderr)
        continue
    with open(file, "rb") as f:
        name = file.name
        checksum = hashlib.sha512(f.read()).hexdigest()
        print(f"adding {name}: {checksum}")
        curr.append([name, checksum])


with open(output, "w", newline="") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(fields)
    writer.writerows(curr)
