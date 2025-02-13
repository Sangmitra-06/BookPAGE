"""
This file performs Named Entity Recognition on the decade subset dataset and saves the extracted entities from
the dataset in a file.
"""

import jsonlines
import spacy

# Load spaCy's small English model for NLP tasks, which includes capabilities for NER.
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    """
    Extract named entities from a given text using spaCy's NLP model.

    :param text: The text from which to extract entities.

    :returns list: A list of tuples containing entity text and its label.
    """
    # Process the input text using spaCy to generate a doc object with NER info
    doc = nlp(text)
    # Extract the text and the label (entity type) of each recognized entity in the document
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities  # Return the list of extracted entities (text, label)


def process_dataset(dataset):
    """
    Process a decade subset dataset to extract named entities from each message in the dataset.

    :param dataset: A list of entries, where each entry contains messages.

    :returns list: A list of dictionaries, each containing the extracted entities from a message.
    """
    extracted_entities = []  # Initialize a list to store the extracted entities from each dataset entry
    for entry in dataset:
        # Get the list of messages from the dataset entry, default to an empty list if not found
        messages = entry.get("messages", [])
        for message in messages:
            # Get the content of each message, default to an empty string if no content is available
            content = message.get("content", "")
            # Extract entities from the content of the message
            entities = extract_entities(content)
            # If any entities were found, append them to the extracted_entities list
            if entities:
                extracted_entities.append({"entities": entities})
    return extracted_entities  # Return the list of all extracted entities


# Input and output file paths
input_file = 'path to input dataset'  # Path to the dataset in JSON Lines format
output_file = 'path to output file'  # Path where extracted entities will be saved

# Read the input dataset from a JSON Lines file
try:
    # Open the input file using jsonlines in read mode and load all the data into a list
    with jsonlines.open(input_file, 'r') as reader:
        dataset = list(reader)
except FileNotFoundError:
    # If the input file is not found, print an error message and exit the program
    print(f"Error: Input file '{input_file}' not found.")
    exit(1)

# Process the dataset to extract named entities from each message
extracted_entities = process_dataset(dataset)

# Write the extracted entities to a JSON Lines output file
try:
    # Open the output file using jsonlines in write mode and write all extracted entities to it
    with jsonlines.open(output_file, 'w') as writer:
        writer.write_all(extracted_entities)
    # Notify the user that the extraction and saving were successful
    print(f"Extracted entities saved to '{output_file}'.")
except Exception as e:
    # If an error occurs during file writing, print the error message
    print(f"Error occurred while saving the extracted entities: {e}")