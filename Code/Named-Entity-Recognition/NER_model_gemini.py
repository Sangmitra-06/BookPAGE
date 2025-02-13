"""
This file queries Gemini and extracts the entities from each response. Subsequently,
it compares the entities to those present in the decade subset.
"""

# Load spaCy model
nlp = spacy.load("en_core_web_sm")  # Load the small English model provided by spaCy

# Initialize Vertex AI client
vertexai.init(project="replace with project id", location="your location")  # Initialize Vertex AI with the given project and location

# File to save the results
results_file = "path to result file"  # Specify the file to save the results of matched entities
entities_file = "path to file containing the decade entities"  # Specify the file containing extracted entities to use as ground truth


# Function to extract entities from text using spaCy
def extract_entities(text):
    """
    Extract named entities from the given text using spaCy.

    :param text: The input text from which to extract entities.

    :returns list: A list of tuples where each tuple contains the entity text and its label.
    """
    doc = nlp(text)  # Process the text using spaCy
    return [(ent.text, ent.label_) for ent in doc.ents]  # Return a list of entities as tuples (text, label)


# Load entities from JSONL file
def load_entities_from_jsonl(jsonl_file):
    """
    Load entities from a JSON Lines file.

    :param jsonl_file: Path to the JSON Lines file containing entities.

    :returns list: A list of entities (each entity as a tuple containing text and label).
    """
    entities = []  # Initialize an empty list to store entities
    try:
        with jsonlines.open(jsonl_file) as reader:  # Open the JSON Lines file in read mode
            for obj in reader:  # Iterate through each line (object) in the file
                entities.extend(obj["entities"])  # Append the entities to the list
    except Exception as e:
        print(f"Error loading entities from JSONL file: {e}")  # Print an error message if an exception occurs
    return entities  # Return the list of loaded entities


# Function to count matched entities
def count_matched_entities(model_output_entities, ground_truth_entities):
    """
    Count how many entities from the model output match the ground truth entities.

    :param model_output_entities: List of entities output by the model.
    :param ground_truth_entities: List of ground truth entities from the decade dataset to compare against.

    :returns tuple: The count of matched entities and a list of matched entities (as tuples).
    """
    matched_count = 0  # Initialize the count of matched entities
    matched_entities = []  # Initialize a list to store matched entities
    # Iterate through each entity extracted from the model output
    for entity_model, entity_type_model in model_output_entities:
        # Iterate through each entity in the ground truth data
        for entity_jsonl, entity_type_jsonl in ground_truth_entities:
            # Check if the entity text and entity type match between model output and ground truth
            if entity_model == entity_jsonl and entity_type_model == entity_type_jsonl:
                matched_count += 1  # Increment the matched count
                matched_entities.append((entity_model, entity_type_model))  # Add the matched entity to the list
                break  # Break to prevent counting the same match multiple times
    return matched_count, matched_entities  # Return the count of matched entities and the list of matches


# Function to query Gemini model and count matched entities
def query_and_count_matched_entities(prompt, model_name="model name", num_iterations=20):
    """
    Query the Gemini model multiple times and compare its output to ground truth entities.
    Calculate how many entities match between the model output and the ground truth.

    :param prompt: The prompt to send to the Gemini model.
    :param model_name: The name of the model to query (default is "gemini-1.0-pro").
    :param num_iterations: The number of times to query the model.

    :returns tuple: The average matched entity count and a list of matched entities.
    """
    total_matched_count = 0  # Initialize total matched count across all iterations
    total_matched_entities = []  # Initialize a list to store all matched entities across iterations
    successful_iterations = 0  # Initialize a counter for successful model queries
    ground_truth_entities = load_entities_from_jsonl(entities_file)  # Load ground truth entities from JSONL file

    # If no ground truth entities were loaded, print a message and exit the function
    if not ground_truth_entities:
        print("No ground truth entities found. Exiting.")
        return 0, []  # Return 0 matched count and an empty list

    model = GenerativeModel(model_name)  # Initialize the Gemini generative model
    chat = model.start_chat(response_validation=False)  # Start a chat session with the model

    # Set the generation configuration with specific settings for output tokens and randomness
    generation_config = {
        "max_output_tokens": 1000,  # Set maximum tokens for model output
        "temperature": 1.5,  # Increase randomness in model output
        "top_p": 1,  # Ensure diverse output by considering the top options
    }

    # Loop to query the model multiple times (num_iterations)
    for i in range(num_iterations):
        print(f"Iteration {i + 1}...")  # Print the iteration number
        try:
            response = chat.send_message(prompt, generation_config=generation_config)  # Query the model
            model_output = response.text  # Get the model's response as text
            print(f"Model response (Iteration {i + 1}): {model_output}")  # Print the model response

            # Extract entities from the model's response
            model_output_entities = extract_entities(model_output)

            # Count how many entities match between model output and ground truth
            matched_count, matched_entities = count_matched_entities(model_output_entities, ground_truth_entities)
            print(f"Matched entities (Iteration {i + 1}): {matched_entities}")  # Print the matched entities
            total_matched_count += matched_count  # Accumulate the matched count
            total_matched_entities.extend(matched_entities)  # Add the matched entities to the total list
            successful_iterations += 1  # Increment the counter for successful iterations
        except Exception as e:
            print(f"Error: {str(e)}")  # Print an error message if the query fails
        time.sleep(30)  # Add a delay between iterations to avoid rate limiting

    # Calculate the average matched count based on successful iterations
    average_matched_count = total_matched_count / successful_iterations if successful_iterations > 0 else 0
    results = {
        "prompt": prompt,
        "average_matched_count": average_matched_count,
        "total_matched_entities": total_matched_entities
    }
    save_results(results)  # Save the results to the results file
    return average_matched_count, total_matched_entities  # Return the average matched count and the total matches


# Function to save results to JSONL file
def save_results(results):
    """
    Save the results of the model queries and matched entities to a JSON Lines file.

    :param results: A dictionary containing the results to be saved.
    """
    try:
        with jsonlines.open(results_file, mode='a') as writer:  # Open the results file in append mode
            writer.write(results)  # Write the results to the file
        print(f"Results saved successfully: {results}")  # Print a success message
    except Exception as e:
        print(f"Error saving results: {e}")  # Print an error message if saving fails


# Run main process
if __name__ == "__main__":
    # EEP
    user_prompt = "Complete the sentence: Did he have a roommate, a credit card, a habit? I stepped around a junkie in the stairwell and climbed to the second floor. I walked in the room and saw "
    print("Starting process...")  # Print a message indicating the start of the process

    # Run the query and counting process with the specified prompt and number of iterations
    average_matched_count, matched_entities = query_and_count_matched_entities(prompt=user_prompt, num_iterations=20)

    # Print the average matched entity count and the total matched entities
    print("Average Matched Entity Count:", average_matched_count)
    print("Total Matched Entities:")
    for entity, entity_type in matched_entities:
        print(f"{entity} ({entity_type})")  # Print each matched entity and its type