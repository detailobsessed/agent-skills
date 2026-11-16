#!/usr/bin/env python3
"""Sum a numeric column in a CSV file."""

import argparse
import csv
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("column")
    parser.add_argument("--delimiter", default=",")
    parser.add_argument("--no-header", action="store_true")
    args = parser.parse_args()

    total = 0.0
    with open(args.file, newline="") as handle:
        reader = csv.reader(handle, delimiter=args.delimiter)
        if args.no_header:
            index = int(args.column) - 1
        else:
            index = next(reader).index(args.column)
        for number, row in enumerate(reader, start=1):
            cell = row[index].strip()
            if not cell:
                continue
            try:
                total += float(cell)
            except ValueError:
                sys.exit(f"row {number}: not a number: {cell!r}")
    print(total)


if __name__ == "__main__":
    main()
