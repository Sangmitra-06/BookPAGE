# STEP 3: Change the assistant and user to have the completion format.

import jsonlines

def process_dataset(dataset):
    """
    Processes a single dataset entry by modifying the user's content to prompt the completion of a sentence,
    and adjusting the assistant's response accordingly.

    :param dataset: A dataset entry containing a list of messages with 'role' and 'content'.

    :returns dict: The modified dataset with adjusted 'user' and 'assistant' messages.
    """
    assistant_content = None
    user_content = None

    # Loop through the messages to find the assistant's and user's content
    for message in dataset["messages"]:
        if message.get("role") == "assistant":
            assistant_content = message.get("content", "")  # Extract assistant's content
        elif message.get("role") == "user":
            user_content = message.get("content", "")  # Extract user's content

    # If assistant's content is missing, print a warning and return the original dataset
    if not assistant_content:
        print("Assistant's content not found in the dataset.")
        return dataset

    # Extract the first 15 words from the assistant's content
    assistant_words = assistant_content.split()  # Split the assistant's response into words
    first_15_words_assistant = ' '.join(assistant_words[:15])  # Get the first 15 words
    remaining_content_assistant = ' '.join(assistant_words[15:])  # Get the rest of the assistant's content

    # Initialize a list to store the modified messages and a flag to track user content modification
    modified_messages = []
    user_content_modified = False

    # Loop through the messages again to modify them
    for message in dataset["messages"]:
        if message.get("role") == "user":
            if not user_content_modified:
                # Modify the user's message to include a prompt based on the first 15 words of assistant's content
                user_content = f"Complete the sentence: {first_15_words_assistant}{user_content[len(first_15_words_assistant):]}"
                modified_message = {"role": "user", "content": user_content}
                modified_messages.append(modified_message)  # Append the modified user message
                user_content_modified = True  # Set the flag to True so the user message is only modified once
        elif message.get("role") == "assistant":
            # Modify the assistant's message to contain only the remaining content after the first 15 words
            modified_message = {"role": "assistant", "content": remaining_content_assistant}
            modified_messages.append(modified_message)  # Append the modified assistant message
        else:
            modified_messages.append(message)  # Keep all other messages unchanged

    # Ensure the assistant's content is not empty in the modified dataset
    for i, message in enumerate(modified_messages):
        if message.get("role") == "assistant" and not message.get("content"):
            # If the assistant's content is empty, copy the user's content as a fallback
            for msg in modified_messages:
                if msg.get("role") == "user":
                    modified_messages[i]["content"] = msg["content"]
                    break

    # Update the dataset with the modified messages
    dataset["messages"] = modified_messages
    return dataset


# Input and output file paths
input_file = 'path to input jsonl file'  # Path to the input JSON Lines file
output_file = 'path to output file'  # Path to the output JSON Lines file

# Read input dataset from JSON Lines file
try:
    with jsonlines.open(input_file, 'r') as reader:
        dataset = list(reader)  # Read all entries from the JSON Lines file
except FileNotFoundError:
    # Handle the case when the input file is not found
    print(f"Error: Input file '{input_file}' not found.")
    exit(1)

# Process each entry in the dataset
modified_datasets = []
for data in dataset:
    modified_data = process_dataset(data)  # Modify the dataset entry
    modified_datasets.append(modified_data)  # Append the modified dataset to the list

# Write modified datasets to the output JSON Lines file
try:
    with jsonlines.open(output_file, 'w') as writer:
        writer.write_all(modified_datasets)  # Write all modified datasets to the output file
    print(f"Modified dataset saved to '{output_file}' in JSON Lines format.")  # Success message
except Exception as e:
    # Handle any errors that occur while saving the file
    print(f"Error occurred while saving the modified dataset: {e}")
