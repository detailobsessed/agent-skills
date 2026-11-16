# csvsum

Sums a numeric column in a CSV file. I wrote it because I kept opening a spreadsheet just to add up one column of an export.

## Install

Copy `csvsum.py` somewhere on your `PATH` and make it executable. It needs Python 3.10 or newer and nothing else.

## Usage

```sh
csvsum.py orders.csv amount
```

prints the sum of the `amount` column. Empty cells are skipped. A cell that is not a number stops the run with an error naming the row.

## Options

| Option | Meaning |
| --- | --- |
| `--delimiter CHAR` | field separator, default `,` |
| `--no-header` | treat the first row as data; refer to columns by number from 1 |

## License

MIT
