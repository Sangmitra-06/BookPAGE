from scipy.spatial.distance import cosine
import numpy as np
from glove import Corpus, Glove
from nltk.tokenize import word_tokenize

# Define the words for the groups and role set, examples are provided below for the role of homemaker
male_words = ["man", "father", "brother"]
female_words = ["woman", "mother", "sister"]
non_binary_words = ["they", "them", "partner"]
homemaker_words = ["homemaker", "family", "caregiver", "cooking"]

glove_model = Glove.load('path to glove model')
# Get vectors for words in each group and homemaker set
def get_vectors(words, model):
    return [model.word_vectors[model.dictionary[word]] for word in words if word in model.dictionary]

male_vectors = get_vectors(male_words, glove_model)
female_vectors = get_vectors(female_words, glove_model)
non_binary_vectors = get_vectors(non_binary_words, glove_model)
homemaker_vectors = get_vectors(homemaker_words, glove_model)

# Compute the association score for each group
def compute_association(group_vectors, attribute_vectors):
    return np.mean([1 - cosine(w, a) for w in group_vectors for a in attribute_vectors])

male_association = compute_association(male_vectors, homemaker_vectors)
female_association = compute_association(female_vectors, homemaker_vectors)
non_binary_association = compute_association(non_binary_vectors, homemaker_vectors)

print("Male association with homemaker:", male_association)
print("Female association with homemaker:", female_association)
print("Non-binary association with homemaker:", non_binary_association)
