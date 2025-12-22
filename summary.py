import csv
from collections import Counter
import argparse
import os

def count_column_entries(file_path, column_name, split_delimiter=None):
    counter = Counter()
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        if column_name not in reader.fieldnames:
            raise ValueError(f"Column '{column_name}' not found in CSV. Available columns: {reader.fieldnames}")

        for row in reader:
            entry = row.get(column_name)
            if entry:
                if split_delimiter:
                    items = entry.split(split_delimiter)
                    items = [item.strip() for item in items if item.strip()]
                    counter.update(items)
                else:
                    counter[entry.strip()] += 1
    
    return counter

def get_input_or_prompt(args):
    file_path = args.file or input("Enter the path to the CSV file: ").strip()
    while not os.path.isfile(file_path):
        print("File not found. Try again.")
        file_path = input("Enter the path to the CSV file: ").strip()
    
    column_name = args.column or input("Enter the column name to analyze: ").strip()
    split_delimiter = args.split if args.split is not None else input("Enter a delimiter to split entries (leave blank if none): ").strip()
    split_delimiter = split_delimiter if split_delimiter else None

    return file_path, column_name, split_delimiter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count occurrences in a CSV column.")
    parser.add_argument("--file", help="Path to the CSV file")
    parser.add_argument("--column", help="Name of the column to analyze")
    parser.add_argument("--split", help="Delimiter to split entries (e.g., '; ' for authors)", default=None)

    args = parser.parse_args()
    file_path, column_name, split_delimiter = get_input_or_prompt(args)

    try:
        counts = count_column_entries(file_path, column_name, split_delimiter)
        for item, count in counts.most_common():
            print(f"{item}: {count}")
    except Exception as e:
        print(f"Error: {e}")
