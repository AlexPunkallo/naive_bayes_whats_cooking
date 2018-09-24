
# coding: utf-8

import json
from collections import Counter
import pandas as pd

with open('train.json') as data_file: 
    train = json.load(data_file)
with open('test.json') as data_file: 
    test = json.load(data_file)

Prob_C ={}
cousines = [item["cuisine"] for item in train]
cous_count  = dict(Counter(cousines))

for key in cous_count:    
    Prob_C[key] = float(cous_count[key])/float(len(cousines))    

dict_cuis = {}
dict_cuis = {cuis: [] for cuis in Prob_C.keys()}
for item in train:
    dict_cuis[item['cuisine']].extend(item['ingredients'])

Prob_I_C = { cuis  : dict(Counter(dict_cuis[cuis])) for cuis in dict_cuis}
output = pd.DataFrame(columns=["id", "cuisine"])

for item in test:
    max = 0
    max_cuis = ""
    for cuis in Prob_C.keys():
        prob = Prob_C[cuis]
        for ingr in item["ingredients"]:
            if ingr in Prob_I_C[cuis].keys():
                prob*=Prob_I_C[cuis][ingr]
            else:
                prob*=10**-6
        if prob>max:
            max = prob
            max_cuis = cuis    
    output = output.append({"id": int(item["id"]), "cuisine": max_cuis}, ignore_index=True)
    
output.id = output.id.astype(int)
output.to_csv("output.csv", index=False)

