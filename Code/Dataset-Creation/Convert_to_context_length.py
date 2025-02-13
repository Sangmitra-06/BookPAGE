# STEP 2: convert the jsonl from the anyscale format to segmented instances.

import json

# Function to split text into chunks of maximum length without skipping words
def split_text_into_chunks(text, max_length):
    """
    Splits a long text into smaller chunks, ensuring that no chunk exceeds the
    maximum length while keeping the words intact.

    :param text: The full text to be split into chunks.
    :param max_length: The maximum character length of each chunk.

    :returns list: A list of text chunks, each chunk within the specified maximum length.
    """
    words = text.split()  # Split the text into words
    chunks = []  # List to store text chunks
    current_chunk = []  # List to accumulate words for the current chunk

    # Loop through each word in the text
    for word in words:
        # Check if adding the next word exceeds the maximum chunk length
        if sum(len(word) + 1 for word in current_chunk) + len(word) <= max_length:
            current_chunk.append(word)  # Add the word to the current chunk
        else:
            # If the current chunk exceeds max_length, join the words into a chunk and append it
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]  # Start a new chunk with the current word

    # If there are any remaining words in current_chunk, add them as the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks  # Return the list of chunks

# Input and output file paths
input_file_path = "path to input jsonl file"  # Path to the input JSONL file
output_file_path = "path to output file"  # Path to the output segmented JSONL file

# Maximum length of each chunk in characters
max_chunk_length = 500  # Maximum chunk size

# Prepare segmented dataset in JSONL format
with open(input_file_path, "r", encoding="utf-8") as in_file, open(output_file_path, "w", encoding="utf-8") as out_file:
    # Loop through each line in the input file
    for line in in_file:
        try:
            # Load JSON object from the current line
            instance = json.loads(line)
        except json.JSONDecodeError as e:
            # If there's an error decoding the JSON, print a message and skip the line
            print(f"Error decoding JSON on line: {line}")
            continue

        # Check if the JSON object contains a "messages" field
        if "messages" in instance:
            messages = instance["messages"]
            title = None  # Initialize title to None

            # Extract title from user message content
            for message in messages:
                if message["role"] == "user":  # Check if the message role is "user"
                    content = message["content"]
                    # Locate the title within the user message by finding the quotes
                    title_start = content.find("'") + 1
                    title_end = content.rfind("'")
                    if title_start != -1 and title_end != -1:
                        title = content[title_start:title_end]  # Extract the title
                    break  # Stop searching once the title is found

            if title:
                # Check if the last message in the messages list is from the assistant
                if "assistant" in messages[-1]["role"]:
                    content = messages[-1]["content"]  # Get the content of the assistant message

                    # Split the content into chunks that do not exceed the max_chunk_length
                    content_chunks = split_text_into_chunks(content, max_chunk_length)

                    # Create new JSONL entries for each chunk with the consistent title
                    for chunk in content_chunks:
                        # Recreate the conversation structure for each chunk
                        system_message = {
                            "role": "system",
                            "content": "You are a helpful assistant. Provide an answer to the following question."
                        }
                        user_message = {
                            "role": "user",
                            "content": f"Write an excerpt of the book '{title}' ."
                        }
                        assistant_message = {
                            "role": "assistant",
                            "content": chunk
                        }
                        # Bundle the messages into the correct format
                        messages = [system_message, user_message, assistant_message]
                        json_entry = {"messages": messages}
                        # Write the new JSONL entry (one line per chunk)
                        out_file.write(json.dumps(json_entry) + "\n")
            else:
                # If the title cannot be found in the user message, print a warning message
                print("Title not found in user message content.")

print("Segmentation completed. Segmented dataset saved to:", output_file_path)  # Output success message
