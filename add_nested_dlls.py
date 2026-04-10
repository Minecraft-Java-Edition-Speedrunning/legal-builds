import argparse
import csv
import hashlib
import pathlib
import sys

OUTPUT = pathlib.Path(__file__).with_name("legal-dlls.csv")
VALID_SUFFIXES = {".dll", ".dylib", ".so"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Recursively add .dll, .dylib, and .so files to legal-dlls.csv "
            "using the provided version."
        )
    )
    parser.add_argument("version", help="Version string to store in legal-dlls.csv")
    parser.add_argument("directory", help="Directory to scan recursively for native libraries")
    return parser.parse_args()


def load_existing_rows() -> tuple[list[str], list[list[str]]]:
    with OUTPUT.open("r", newline="") as file:
        reader = csv.reader(file)
        fields = next(reader)
        rows = list(reader)
    return fields, rows


def iter_library_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in VALID_SUFFIXES
    )


def sha512_for_file(path: pathlib.Path) -> str:
    with path.open("rb") as file:
        return hashlib.sha512(file.read()).hexdigest()


def main() -> int:
    args = parse_args()
    root = pathlib.Path(args.directory)
    if not root.exists():
        print(f"{root}: directory does not exist!", file=sys.stderr)
        return 1
    if not root.is_dir():
        print(f"{root}: expected a directory!", file=sys.stderr)
        return 1

    fields, rows = load_existing_rows()
    library_files = iter_library_files(root)
    if not library_files:
        print(f"{root}: no .dll, .dylib, or .so files found!", file=sys.stderr)
        return 1

    for file in library_files:
        checksum = sha512_for_file(file)
        relative_path = file.relative_to(root)
        print(f"adding {file.name} {args.version}: {relative_path} -> {checksum}")
        rows.append([file.name, args.version, checksum])

    with OUTPUT.open("w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)

    print(f"added {len(library_files)} file(s) to {OUTPUT.name}")
    return 0


main()