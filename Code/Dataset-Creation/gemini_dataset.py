# Convert the dataset to gemini format.

import json


def replace_role_in_jsonl(input_file, output_file):
    """
    Reads a JSONL file line by line, replacing the 'role' from 'assistant' to 'model'
    in each message, and writes the modified data to an output file.

    :param input_file: Path to the input JSONL file.
    :param output_file: Path to the output JSONL file where modified data will be saved.
    """
    # Open the input file for reading and output file for writing
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # Loop through each line in the input file
        for line in infile:
            data = json.loads(line)  # Parse the JSON object from the current line
            # Iterate through the messages in the 'messages' field of the JSON object
            for message in data['messages']:
                # If the 'role' is 'assistant', change it to 'model'
                if message['role'] == 'assistant':
                    message['role'] = 'model'
            # Write the modified JSON object back to the output file in JSONL format
            outfile.write(json.dumps(data) + '\n')


# Define the input and output file paths
input_file = 'path to jsonl file'  # Path to the original JSONL dataset
output_file = 'path to output file'  # Path to save the modified dataset

# Call the function to process the dataset and replace 'assistant' roles with 'model'
replace_role_in_jsonl(input_file, output_file)

