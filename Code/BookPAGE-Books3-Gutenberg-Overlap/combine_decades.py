"""
    This file combines the individual decade specific files of overlapped and non overlapped books into two files,
    one containing all overlapped books and one containing non-overlapped books. This is step 2, run after running
    overlapped_and_nonoverlapped_decade.py
"""

import json
import os

def combine_json_files(file_prefix, decades, base_path):
    """
    Combines JSON files that have a common prefix and are differentiated by decades.

    :param file_prefix: Prefix of the files to combine ('overlapped_' or 'non_overlapped_').
    :param decades: List of decade strings, e.g., ['1950-1959', '1960-1969', ...].
    :param base_path: Directory where the files are located.

    :returns: list: Combined list of all data from the files.
    """
    combined_data = []
    for decade in decades:
        file_path = os.path.join(base_path, f"{file_prefix}{decade}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                combined_data.extend(data)
        else:
            print(f"File not found: {file_path}")
    return combined_data

def save_combined_json(data, output_file):
    """
    Saves combined data to a JSON file.

    :param data: Data to save.
    :param output_file (str): Path to the output file.
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data successfully saved to {output_file}")

# Define the base path and decade ranges
base_path = 'specify your base path'
decades = ['1950-1959', '1960-1969', '1970-1979', '1980-1989', '1990-1999', '2000-2009', '2010-2019']

# Combine and save overlapped titles into one JSON
overlapped_data = combine_json_files('overlapped_', decades, base_path)
save_combined_json(overlapped_data, os.path.join(base_path, 'combined_overlapped.json'))

# Combine and save non-overlapped titles into another JSON
non_overlapped_data = combine_json_files('non_overlapped_', decades, base_path)
save_combined_json(non_overlapped_data, os.path.join(base_path, 'combined_non_overlapped.json'))
