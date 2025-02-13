"""
STEP 1: Convert from json to jsonl with the system, user, and assistant format.
"""

import json


# Function to convert each entry into the format required with 'system', 'user', and 'assistant' roles.
def convert_to_msg(entry):
    """
    Converts a single dataset entry into the 'system', 'user', and 'assistant' format.

    :param entry: A dictionary containing the 'title' and 'content' of a book.

    :returns dict: A dictionary with the conversation structure including system, user, and assistant.
    """
    # Define the system prompt to instruct the assistant's behavior
    system_prompt = "You are a helpful assistant. Provide an answer to the following question."

    # Create a user prompt asking for an excerpt from the book using the title of the book
    user_prompt = f"Write an excerpt of the book '{entry['title']}' ."

    # Use the content of the book as the assistant's response
    assistant_response = entry['content']

    # Return the formatted message with roles 'system', 'user', and 'assistant'
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_response}
        ]
    }


# Function to load a JSON file, convert its entries, and save them in JSONL format
def convert_dataset_to_jsonl(input_file, output_file):
    """
    Reads the dataset from a JSON file, converts it into message format, and writes it to a JSONL file.

    :param input_file: The path to the input JSON file containing the dataset.
    :param output_file: The path to the output JSONL file to save the converted data.
    """
    # Open the input file and load the dataset from JSON
    with open(input_file, 'r', encoding='utf-8') as infile:
        dataset = json.load(infile)  # Read and parse the JSON file

    # Open the output file for writing the converted data in JSONL format
    with open(output_file, 'w') as outfile:
        # Loop through each entry in the dataset
        for entry in dataset:
            # Convert the current entry to the message format
            json_line = convert_to_msg(entry)
            # Write the converted entry as a JSON object to the output file
            json.dump(json_line, outfile)
            outfile.write('\n')  # Write a newline to separate each entry (JSONL format)


# Define the input and output file paths
input_file_path = 'path to input dataset in json'  # Path to the input dataset in JSON format
output_file_path = 'path to output file'  # Path to save the converted dataset in JSONL format

# Call the function to convert the dataset and write it to the output file
convert_dataset_to_jsonl(input_file_path, output_file_path)

# Print a success message when the conversion is complete
print(f"Dataset successfully converted to JSON Lines format. Saved to: {output_file_path}")
