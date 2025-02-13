"""
    This file finds overlapped titles between each decade of BookPAGE and Project Gutenberg
"""

import os  # Module for interacting with the file system
import re  # Module for regular expression matching
import rdflib  # Library for working with RDF (Resource Description Framework) data
from tqdm import tqdm  # Library for displaying progress bars


def parse_titles(file_path):
    """
    Parse book titles and group them by decade from a text file.

    :param file_path: The path to the text file containing book titles.

    :returns: dict: A dictionary where each key is a decade (str) and its value is a list of book titles (list of str).
    """
    decade_pattern = re.compile(r"^\d{4}-\d{4}$")  # Regular expression to match decade strings (e.g., "1990-1999")
    title_pattern = re.compile(r"^(.+) by (.+)$")  # Regular expression to match book titles (e.g., "Title by Author")

    decades = {}  # Dictionary to store titles grouped by decade
    current_decade = None  # Variable to track the current decade

    with open(file_path, 'r', encoding='utf-8') as file:  # Open the file for reading
        for line in file:  # Iterate through each line in the file
            line = line.strip()  # Remove leading/trailing whitespace
            if decade_pattern.match(line):  # Check if the line matches the decade pattern
                current_decade = line  # Set the current decade
                decades[current_decade] = []  # Initialize an empty list for the current decade
            elif title_pattern.match(
                    line) and current_decade:  # Check if line matches title pattern and a decade is set
                title = title_pattern.match(line).group(1)  # Extract the title from the matched line
                decades[current_decade].append(title)  # Append the title to the current decade's list

    return decades  # Return the dictionary of decades with associated titles


def save_titles_to_file(titles, filename='gutenberg_titles.txt'):
    """
    Save a set of book titles to a file, sorted alphabetically.

    :param titles: A set of book titles to save.
    :param filename: The name of the output file. Defaults to 'gutenberg_titles.txt'.
    """
    with open(filename, 'w', encoding='utf-8') as file:  # Open file for writing
        for title in sorted(titles):  # Sort titles alphabetically for easier reading and consistency
            file.write(title + '\n')  # Write each title to a new line in the file
    print(f"Titles have been saved to {filename}")  # Notify the user that the file has been saved


def parse_rdf_files(directory_path):
    """
    Parse RDF files in a directory to extract Gutenberg book titles.

    :param directory_path: The path to the directory containing RDF files.

    :returns: set: A set of unique Gutenberg titles extracted from the RDF files.
    """
    gutenberg_titles = set()  # Use a set to store unique Gutenberg titles
    PGTERMS = rdflib.Namespace('http://www.gutenberg.org/2009/pgterms/')  # RDF namespace for Gutenberg terms
    DCTERMS = rdflib.Namespace('http://purl.org/dc/terms/')  # RDF namespace for Dublin Core metadata terms

    # Collect all .rdf file paths from the specified directory and subdirectories
    files_to_process = [os.path.join(root, file) for root, dirs, files in os.walk(directory_path) for file in files if
                        file.endswith('.rdf')]

    for rdf_path in tqdm(files_to_process, desc="Processing RDF Files"):  # Show progress bar while processing files
        g = rdflib.Graph()  # Create a new RDF graph for each file
        g.parse(rdf_path)  # Parse the RDF file
        # Iterate through all subjects of type PGTERMS.ebook (books)
        for book in g.subjects(rdflib.RDF.type, PGTERMS.ebook):
            title = str(g.value(book, DCTERMS.title))  # Extract the book title
            if title:  # If a title is found, add it to the set
                gutenberg_titles.add(title)

    save_titles_to_file(gutenberg_titles)  # Save the extracted titles to a file
    return gutenberg_titles  # Return the set of Gutenberg titles


def calculate_overlap(user_titles, gutenberg_titles):
    """
    Calculate the overlap (as a percentage) between BookPAGE titles and Gutenberg titles for each decade.

    :param user_titles: A dictionary of BookPAGE titles, grouped by decade.
    :param gutenberg_titles: A set of Gutenberg titles to compare against.

    :returns dict: A dictionary where each key is a decade (str) and the value is the overlap percentage (float).
    """
    overlaps = {}  # Dictionary to store the overlap percentages by decade
    for decade, titles in user_titles.items():  # Iterate through each decade in user-provided titles
        user_set = set(titles)  # Convert the list of titles for the decade into a set
        overlap_count = len(user_set & gutenberg_titles)  # Calculate the intersection (overlap) between the two sets
        total_titles = len(user_set)  # Get the total number of titles for the decade
        # Calculate overlap percentage, avoid division by zero
        overlap_percentage = (overlap_count / total_titles) * 100 if total_titles > 0 else 0
        overlaps[decade] = overlap_percentage  # Store the overlap percentage for the decade
    return overlaps  # Return the dictionary of overlap percentages


# Specify the file path and the directory containing RDF files
file_path = 'books.txt'  # Path to the text file containing user-provided titles
rdf_directory_path = 'rdf-files'  # Path to the directory containing Gutenberg RDF files

# Parse titles by decade from the user's text file
decades_dict = parse_titles(file_path)  # Call the function to parse the user-provided titles

# Parse RDF files to get Gutenberg titles (as a set of titles)
gutenberg_titles = parse_rdf_files(rdf_directory_path)  # Call the function to extract titles from RDF files

# Calculate overlaps between user-provided titles and Gutenberg titles
overlap_percentages = calculate_overlap(decades_dict, gutenberg_titles)  # Call the function to calculate overlaps
print(overlap_percentages)  # Print the overlap percentages by decade
