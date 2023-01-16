import json

import numpy as np


## this function will read json files and return the values of the branch ur interessted in
def get_json(filename: str, tag: str = None, major_dic: str = None):
    ## here u should pass the file name correctly
    try:
        if filename[-5:] != ".json":
            with open(filename + ".json") as f:
                dt = json.load(f)
        elif filename[-5:] == ".json":
            with open(filename) as f:
                dt = json.load(f)
    ## checking if the file is not json
    except filename[-4:] != "json":
        raise ("Sorry only Json files")
    ## the list where we are going to store the names as strings extracted from the dictionary
    new_dict = list()
    if major_dic is not None:
        for i in dt[major_dic]:
            pass
        for x in i[tag]:
            new_dict.append(x)
    else:
        for i in dt:
            new_dict.append(i[tag])
    ## return the selected line as list
    return np.array(new_dict).flatten()
