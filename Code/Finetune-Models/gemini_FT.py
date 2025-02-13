# Initiate the fine-tuning process for Gemini
import time

import vertexai
from vertexai.preview.tuning import sft

# Initialize Vertex AI environment with the project ID and location
# This is where the fine-tuning job will run
vertexai.init(project='your project id', location="your location")
# Start a fine-tuning job using the source model and training dataset
sft_tuning_job = sft.train(
    source_model="source model name",  # Specify the source model to fine-tune
    train_dataset="path to your train dataset",  # Path to the training dataset in Google Cloud Storage (JSONL format)
    epochs=4,  # Number of training epochs for fine-tuning
    learning_rate_multiplier=1.0,  # Adjust the learning rate by this multiplier
    tuned_model_display_name="saved model name",  # Name to display for the fine-tuned model
)

# Polling loop to check the status of the tuning job until it's completed
while not sft_tuning_job.has_ended:
    time.sleep(60)  # Wait for 60 seconds before checking the job status again
    sft_tuning_job.refresh()  # Refresh the job status

# Once the tuning job is completed, print the resulting fine-tuned model details
print(sft_tuning_job.tuned_model_name)  # Print the name of the fine-tuned model
print(sft_tuning_job.tuned_model_endpoint_name)  # Print the endpoint name for deploying the model
print(sft_tuning_job.experiment)  # Print the experiment details related to this fine-tuning job
