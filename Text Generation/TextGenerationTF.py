##########################################################################################################
## After a long time of Trainig ..we should now load the Model with two Pickle Files and begin using it ##
##########################################################################################################

## import the proper packages 
import pickle
import numpy as np
from keras.layers import LSTM, Dropout, Dense
from keras.models import Sequential 
import tqdm ## tqdm is a library in Python which is used for creating Progress Meters or Progress Bars

## our main Hyperparameters
sequence_length = 100
## Let's load the dictionaries that map each integer to a 
## character and vise-versa that we saved before in the data preparation phase
## Load the two pickle files
char2int = pickle.load(open("review.txt--char2int.pickle", "rb"))
int2char = pickle.load(open("review.txt-int2char.pickle", "rb"))
vocab_size = len(char2int)

## we need to build the Network agian but without training this time with the same Hyperparameters
# building the model
model = Sequential([
    LSTM(256, input_shape=(sequence_length, vocab_size), return_sequences=True),
   Dropout(0.3),
LSTM(256),
Dense(vocab_size, activation="softmax"),
])

## Model's Path
model_path = 'text_generation_model.h5'
### now time to load the model
model.load_weights(model_path)

seed = "i'm strong"
s = seed
n_chars = 400
# generate 400 characters
generated = ""
for i in tqdm.tqdm(range(n_chars), "Generating text"):
    # make the input sequence
    X = np.zeros((1, sequence_length, vocab_size))
    for t, char in enumerate(seed):
        X[0, (sequence_length - len(seed)) + t, char2int[char]] = 1
    # predict the next character
    predicted = model.predict(X)[0]
    # converting the vector to an integer
    next_index = np.argmax(predicted)
    # converting the integer to a character
    next_char = int2char[next_index]
    # add the character to results
    generated += next_char
    # shift seed and the predicted character
    seed = seed[1:] + next_char

print("Seed:", s)
print("Generated text:")
print(generated)


