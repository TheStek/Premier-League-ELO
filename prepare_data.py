import numpy as np
import pandas as pd

from os import listdir
from os.path import isfile, join

mypath = "Data"

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]


match_dataframes = []

for file in files:
	try:
		df = pd.read_csv(f"Data/{file}")
		df["Season"] = file[:-4]
		match_dataframes.append(df)
	except:
		print(file)


combined = pd.concat(match_dataframes)

combined.to_csv("Data/Combined.csv", index = False)



