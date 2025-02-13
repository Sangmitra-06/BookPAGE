# 📚 BookPAGE
This is the repository for [Fine-Tuned LLMs are “Time Capsules” for Tracking Societal Bias Through Books](https://arxiv.org/abs/2502.05331). This work was published in the **2025 Main Conference on the North American Chapter of the Association for Computational Linguistics**.

Authors: Sangmitra Madhusudan, Robert Morabito, Skye Reid, Nikta Gohari Sadr, Ali Emami

## 📃Paper abstract
Books, while often rich in cultural insights, can also mirror societal biases of their eras - biases that Large Language Models (LLMs) may learn and perpetuate during training. We introduce a novel method to trace and quantify these biases using fine-tuned LLMs. We develop BookPAGE, a corpus comprising 593 fictional books across seven decades (1950-2019), to track bias evolution. By fine-tuning LLMs on books from each decade and using targeted prompts, we examine shifts in biases related to gender, sexual orientation, race, and religion. Our findings indicate that LLMs trained on decade-specific books manifest biases reflective of their times, with both gradual trends and notable shifts. For example, model responses showed a progressive increase in the portrayal of women in leadership roles (from 8% to 22%) from the 1950s to 2010s, with a significant uptick in the 1990s (from 4% to 12%), possibly aligning with third-wave feminism. Same-sex relationship references increased markedly from the 1980s to 2000s (from 0% to 10%), mirroring growing LGBTQ+ visibility. Concerningly, negative portrayals of Islam rose sharply in the 2000s (26% to 38%), likely reflecting post-9/11 sentiments. Importantly, we demonstrate that these biases stem mainly from the books' content and not the models' architecture or initial training. Our study offers a new perspective on societal bias trends by bridging AI, literary studies, and social science research.

## 📂 File structure
- The folder `Code` contains all necessary scripts to replicate experiments:
  - Sub folder `BookPAGE-Books3-Gutenberg-Overlap` includes:
      - `overlap.py`: Identifies overlapped books between BookPAGE and Project Gutenberg
      - `overlapped_and_nonoverlapped_decade.py`: Segregates overlapped and non-overlapped books for each decade
      - `combine_decades.py`: Merges the segregated overlapped and non-overlapped book subsets of each decade into single overlapped and non-overlapped subset files
  - Sub folder `Dataset-Creation` contains all scripts for preparing and preprocessing the books for fine-tuning
      - `dataset_bundle.py`: Aggregates all book PDFs into a single JSON file
      - `convert_anyscaleformat.py` and `convert_to_context_length.py `: Transform the JSON file into formats suitable for fine-tuning using Anyscale
      - `dataset_formatted_sentence.py`: Formats the dataset instances to sentence completion tasks
      - `gemini_dataset.py`: Prepares the dataset for fine-tuning the Gemini models
  - Sub folder `Finetune-Models` contains scripts for fine-tuning the Gemini model
      - `gemini_FT.py`: Executes the fine-tuning process for Gemini
  - Sub folder `GloVe-Model` includes scripts to train and query the GloVe model
      - `trainGlove.py`: Trains the GloVe model on the dataset
      - `queryGlove.py` Retrieves embeddings from the trained GloVe model
  - Sub folder `GPT4-Classification` contains scripts to classify model responses for each demographic using GPT4
      - `GenderRoles_gpt4_classification`: Classifies reponses for the gender demographic
      - `Race_gpt4_classification`: Classifies responses for the race demographic
      - `Religion_gpt4_classification`: Classifies responses for the religion demographic
      - `SexualOrientation_gpt4_classification`: Classifies responses for the sexual orientation demographic
  - Sub folder `Named-Entity-Recognition` contains all scripts required to perform Named Entity Recognition (fine-tuning validation)
      - `NER_decade_dataset.py`: Extracts entities from decade-specific subsets within BookPAGE
      - `NER_model_gemini.py`: Identifies entities in Gemini's responses to the EEPs.
      - `NER_model_llama.py`: Identifies entities in Llama's responses to the EEPs.
      - `NER_model_Mixtral.py`: Identifies entities in Mixtral's responses to the EEPs.
  - Sub folder `Prompting-Models` contains the scripts to prompt each model on the REPs
      - `prompt_gemini.py`: Prompts Gemini on the REPs
      - `prompt_llama.py`: Prompts Llama on the REPs
      - `prompt_mixtral.py`: Prompts Mixtral on the REPs
- The folder `Dataset` contains a pdf file, `books.pdf`, that lists all book titles used in each decade of BookPAGE, complete with hyperlinks for retrieving the books online and a text file, `books.txt` with book titles in each decade

## 💻 Instructions to Run
1. **Installation**: To install the required dependencies, run the following command:

    ```sh
    pip install -r requirements.txt
    ```

2. **Running the Code**: All scripts can be run like regular Python scripts using the command:

    ```sh
    python script_name.py
    ```

    Replace `script_name.py` with the name of the script you want to run.
