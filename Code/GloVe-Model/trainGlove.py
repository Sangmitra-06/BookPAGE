from glove import Corpus, Glove
from nltk.tokenize import word_tokenize

# File containing your preprocessed dataset (process the dataset to be a text file with one sentence per line)
DATASET_FILE = 'path to preprocessed dataset'

# Parameters for GloVe and Corpus
WINDOW_SIZE = 15  # Context window size
NO_COMPONENTS = 100  # Number of dimensions for word vectors
LEARNING_RATE = 0.05  # Learning rate
EPOCHS = 50  # Number of training epochs
NUM_THREADS = 4  # Number of threads for training

# Load and tokenize dataset
print("Loading and tokenizing dataset...")
with open(DATASET_FILE, 'r', encoding='utf-8') as file:
    sentences = file.readlines()

# Tokenizing each sentence (split into words)
tokenized_sentences = [sentence.strip().lower().split() for sentence in sentences]

# Create a Corpus object
print("Creating corpus...")
corpus = Corpus()

# Fit the corpus with tokenized sentences to generate the co-occurrence matrix
print("Building co-occurrence matrix...")
corpus.fit(tokenized_sentences, window=WINDOW_SIZE)
print(f"Vocabulary size: {len(corpus.dictionary)}")
print(f"Co-occurrence matrix shape: {corpus.matrix.shape}")

# Train the GloVe model
print("Training GloVe model...")
glove = Glove(no_components=NO_COMPONENTS, learning_rate=LEARNING_RATE)
glove.fit(corpus.matrix, epochs=EPOCHS, no_threads=NUM_THREADS, verbose=True)

# Add the dictionary to the GloVe model
glove.add_dictionary(corpus.dictionary)

# Save the GloVe model and dictionary for future use
print("Saving model...")
glove.save('path to save model')
print("Model saved as 'glove_model.model'.")

# Retrieve and display a word embedding
word = "glove"  # Change this to a word in your dataset
if word in glove.dictionary:
    embedding = glove.word_vectors[glove.dictionary[word]]
    print(f"Embedding for '{word}': {embedding}")
else:
    print(f"Word '{word}' not found in vocabulary.")
