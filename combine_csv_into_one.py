"""
CSV Merger

This script combines multiple CSV files into a single large CSV file. The output file includes an
additional column representing the category, which is derived from the input file names.

Usage:
    python3 csv_merger.py
"""

import csv
import glob
import re


def get_category_from_filename(filename: str) -> str:
    """
    Extract the category from a file name.

    Args:
        filename: The name of the file.

    Returns:
        The category as a string.
    """
    category = filename.split(".")[0]
    return " ".join(re.split('-|_', category))


def merge_csv_files(output_file: str) -> None:
    """
    Merge multiple CSV files into a single CSV file.

    Args:
        output_file: The name of the output file.
    """
    with open(output_file, "w", newline='') as output:
        record_writer = csv.writer(output, lineterminator='\n')

        for csv_filename in glob.glob("*.csv"):
            print(csv_filename)
            category = get_category_from_filename(csv_filename)

            with open(csv_filename) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    row.insert(0, category)
                    print(row)

                    record_writer.writerow(row)


if __name__ == "__main__":
    output_csv_file = "combined_large.csv"
    merge_csv_files(output_csv_file)
