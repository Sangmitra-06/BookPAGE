"""
This file is used to concatenate all the pdf files into a dataset of json format. Run this before converting
your files to the required formats.
"""

import os
import json
import pdfplumber


# Function which goes through the entire content in the pdf files and adds it to a string and returns that string. 
def text_from_pdf(path):
    """
    Extracts the text from all pages of a given PDF file.

    :param path: The file path to the PDF file.

    :returns str: A string containing all the text extracted from the PDF.
    """
    with pdfplumber.open(path) as pdf:
        string = ''
        for page in pdf.pages:
            string += page.extract_text()
    return string


# The directory of the pdf files
pdf_directory = 'path to the folder with the pdf files'

# final dataset that is of text format
dataset = []

# finding the number of files for output purposes
num_files = len(os.listdir(pdf_directory))
files_done = 0
print("Total number of files is ",num_files)
# looping through all the files in the directory and concatenating the text into the dataset in the form of "title" and "content"
for file in os.listdir(pdf_directory):
    # For output purposes
    files_done += 1
    print("Processing file "+str(files_done))

    # Getting the path of the file
    path = os.path.join(pdf_directory, file)
    try:
        # using the function to retrieve the text in one pdf
        string = text_from_pdf(path)
    except Exception as e:
        print("Error processing file ",files_done)
        continue

    # Extracting the title of the book from the file name
    title = os.path.splitext(file)[0]

    # adding the book with its title to the final dataset
    dataset.append({"title": title, "content": string})

# Converting the dataset to json format and saving it
# This source was used https://www.geeksforgeeks.org/convert-python-list-to-json/
output_json_file = 'file path'
with open(output_json_file, 'w') as json_file:
    json.dump(dataset, json_file, indent=4)

# for output purposes
print("Dataset saved")
