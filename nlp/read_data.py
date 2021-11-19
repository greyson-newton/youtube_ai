import pandas as pd
import os
import glob
import numpy as np
data=[]
cwd = os.getcwd()
path=cwd+'/data/allsides_data/'
p='/Users/greysonnewton/Desktop/txt-spch/youtube/youtube_ai/nlp/data/allsides_data/all_breaking_news.csv'
df = pd.read_csv(p)
df['is_partisan'] = np.where(df['bias_id']!= 3, False, True)
print(df.describe())

def f(row):
	if row['bias_id'] == 3:
		val = 0
	else:
		val = 1
	return val
df['is_partisan'] = df.apply(f, axis=1)	
print(df)
df.to_csv('/Users/greysonnewton/Desktop/txt-spch/youtube/youtube_ai/nlp/data/allsides_data/partisan_all_breaking_news.csv')
# use glob to get all the csv files 
# in the folder
# csv_files = glob.glob(os.path.join(path, "*.csv"))


# # loop over the list of csv files
# for f in csv_files:

# 	# read the csv file
# 	df = pd.read_csv(f)
	
# 	# print the location and filename
# 	print('Location:', f)
# 	print('File Name:', f.split("\\")[-1])
	
# 	# print the content
# 	print('Content:')
# 	print(df.head(10))
# 	print(df.describe())

