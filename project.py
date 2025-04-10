

import pandas as pd
import chardet

#Since the dataset contains symbols present in European (latin derived) languages a simple "read_csv" was not working.
# Thus, we need to encode our dataset

df= pd.read_csv('data.csv', encoding ='latin1')


#print(df.head())

print(len(df))











