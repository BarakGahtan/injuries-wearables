import pickle

input_file = 'data_dict.pickle'  # File path of the pickle file

# Load the dictionary from the pickle file
with open(input_file, 'rb') as f:
    loaded_dict = pickle.load(f)


x =6