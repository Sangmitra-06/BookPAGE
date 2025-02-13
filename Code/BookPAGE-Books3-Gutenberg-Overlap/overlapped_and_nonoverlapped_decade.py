"""
    This file distinguishes the overlapped and non overlapped books with Books3 for each decade-specific subset in
    BookPAGE. This is step 1, run combine_decades.py to combine all decade specific files into one overlapped and non
    overlapped subset each.
"""

import json
import random
import os

def sanitize_title(title):
    """
    Removes any apostrophes in the title of the books

    :param title: Book title.

    :return string: sanitized book title.
    """
    return title.replace("'", "")

def load_titles(file_path):
    """
    Loads book titles from a file and groups them by decades.

    :param file_path: Path to the file containing book titles
    :return: A dictionary with decades as keys and a list of titles as values.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        titles = {}
        current_decade = None
        for line in file:
            if line.strip() and '-' in line.strip():  # Check for decade line
                current_decade = line.strip()
                titles[current_decade] = []
            elif line.strip():
                sanitized_title = sanitize_title(line.split(" by ")[0].strip())
                titles[current_decade].append(sanitized_title)
    return titles

def select_titles(titles_by_decade, data_dict):
    """
    Selects 7 titles from the titles by decade dictionary that are present in the data dictionary
    representing overlapped or non overlapped decade titles.

    :param titles_by_decade: Dictionary of titles grouped by decade.
    :param data_dict: Dictionary with titles as keys and overlapped or non overlapped book titles as a list.
    :return: A dictionary with selected titles with decades as keys.

    """
    selected_titles = {}
    for decade, titles in titles_by_decade.items():
        available_titles = [title for title in titles if title in data_dict]
        if len(available_titles) >= 7:
            selected_titles[decade] = random.sample(available_titles, 7)
        else:
            selected_titles[decade] = available_titles  # Or handle if not enough titles
    return selected_titles

def load_json_data(json_path):
    """
    Loads data from a JSON file, with book titles as keys.

    :param json_path: Path to the JSON file.
    :return: Dictionary with sanitized titles as keys and their contents as values.
    """
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return {sanitize_title(item['title']): item['content'] for item in data}

def read_json_content(selected_titles, data_dict):
    """
    Extracts content for selected titles from the data dictionary.

    :param selected_titles: A list of selected book titles.
    :param data_dict: Dictionary with book titles and their content.
    :return: A list of dictionaries with selected book titles and their respective contents.
    """
    content = []
    for title in selected_titles:
        book_content = data_dict.get(title, "Content not found")
        content.append({"title": title, "content": book_content})
    return content

def save_to_json(file_path, data):
    """
    Converts a Python dictionary to a JSON file.

    :param file_path: Path where the JSON file will be saved.
    :param data: Data to be saved.
    :return: None.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def process_books(overlapped_path, non_overlapped_path, base_json_path):
    """
    Processes books to separate overlapped and non-overlapped titles for each decade,
    saving results to JSON files.

    :param overlapped_path: Path to the file with overlapped titles.
    :param non_overlapped_path: Path to the file with non-overlapped titles.
    :param base_json_path: Base directory to save the JSON results.
    :return: A tuple containing two dictionaries, one with file paths of results and another with selected titles.
    """
    decade_to_index = {
        '1950-1959': '1', '1960-1969': '2', '1970-1979': '3',
        '1980-1989': '4', '1990-1999': '5', '2000-2009': '6', '2010-2019': '7'
    }

    overlapped_titles = load_titles(overlapped_path)
    non_overlapped_titles = load_titles(non_overlapped_path)

    results = {}
    final_selected_titles = {}  # Dictionary to store final selected titles

    for decade, index in decade_to_index.items():
        json_path = os.path.join(base_json_path, f"dataset{index}_new.json")
        data_dict = load_json_data(json_path)

        selected_overlapped = select_titles({decade: overlapped_titles.get(decade, [])}, data_dict)
        selected_non_overlapped = select_titles({decade: non_overlapped_titles.get(decade, [])}, data_dict)

        overlapped_content = read_json_content(selected_overlapped[decade], data_dict)
        non_overlapped_content = read_json_content(selected_non_overlapped[decade], data_dict)

        # Save to JSON files
        overlapped_file_path = f"overlapped_{decade}.json"
        non_overlapped_file_path = f"non_overlapped_{decade}.json"
        save_to_json(overlapped_file_path, overlapped_content)
        save_to_json(non_overlapped_file_path, non_overlapped_content)

        # Store the selected titles in the final results
        final_selected_titles[decade] = {
            "overlapped_titles": selected_overlapped[decade],
            "non_overlapped_titles": selected_non_overlapped[decade]
        }

        results[decade] = {
            "overlapped_file": overlapped_file_path,
            "non_overlapped_file": non_overlapped_file_path
        }

    return results, final_selected_titles

# Define file paths
overlapped_path = 'text file containing overlapped book titles'
non_overlapped_path = 'text file containing non overlapped book titles'
base_json_path = 'directory to save results'  # Update this to your actual directory

# Execute the processing of books
book_results, final_titles = process_books(overlapped_path, non_overlapped_path, base_json_path)

# Output the final selected titles
for decade, titles_info in final_titles.items():
    print(f"Decade: {decade}")
    print("Final Selected Overlapped Titles:", titles_info['overlapped_titles'])
    print("Final Selected Non-Overlapped Titles:", titles_info['non_overlapped_titles'])
