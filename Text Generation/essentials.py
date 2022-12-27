## That file is used only to get tne target data that we want to apply the NN on from CSV file to Text file

import pandas as pd

## read the data set
dataset = pd.read_csv("IMDB Dataset.csv")

## get the required column
review = list(dataset["review"])


## we need our csv data to be converted to text file
## we only need one column ["review"]
# converting list into string and then joining it with space
b = " ".join(str(e) for e in review)

with open("review.txt", "w", encoding="utf-8") as file:
    file.write(b)
## now the data is ready
