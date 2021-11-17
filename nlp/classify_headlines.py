from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import pandas as pd
import pickle
import re, string, random, os
import playsound

import numpy as np # linear algebra
from sklearn.model_selection import train_test_split # function for splitting data to train and test sets

spin_w_p=['Emerge','Serious','Refuse','Crucial','High-stakes','Tirade','Landmark','Latest in a string of...','Major','Turn up the heat','Critical','Decrying','Offend','Stern talks','Offensive','Facing calls to...','Meaningful','Even though','Monumental','Significant']
implicative_w_p=['Finally','Surfaced','Acknowledged','Emerged','Refusing to say','Conceded','Dodged','Admission','Came to light','Admit to']
emotional_w_p=['Mocked','Raged','Bragged','Fumed','Lashed out','Incensed','Scoffed','Frustration','Erupted','Rant','Boasted','Gloated']
subjective_w_p=['Good','Better','Best','Is considered to be','Seemingly','Extreme','May mean that','Could','Apparently','Bad','Worse','Worst','its likely that','Dangerous','Suggests','Would seem','Decrying','Possibly']
sensational_w_p=['Shocking','Remarkable','Rips','Chaotic','Lashed out','Onslaught','Scathing','Showdown','Explosive','Slams','Forcing','Warning','Embroiled in...','Torrent of tweets','Desperate']

df = pd.read_pickle("/Users/greysonnewton/Desktop/txt-spch/youtube/allsides_training_data/breaking_news.pkl")
df['desc_word_count'] = df['desc.'].apply(lambda x: len(x.strip().split())) 
df['desc_word_count'].describe(include='all')
df = df.sample(1725, random_state=42)
import spacy
from spacy.lang.en.stop_words import STOP_WORDS #import commen list of stopword
nlp = spacy.load("en_core_web_sm")
def spacy_tokenizer(sentence):
    ''' Function to preprocess text of scientific papers 
        (e.g Removing Stopword and puntuations)'''
    mytokens = nlp(sentence)
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ] # transform to lowercase and then split the scentence
    mytokens = [ word for word in mytokens if word not in stopwords and word not in punctuations ] #remove stopsword an punctuation
    mytokens = " ".join([i for i in mytokens]) 
    return mytokens

import string
punctuations = string.punctuation #list of punctuation to remove from text
stopwords = list(STOP_WORDS)
stopwords[:10]  
tqdm.pandas()
df["processed_desc"] = df["desc."].progress_apply(spacy_tokenizer)
def vectorize(text, maxx_features):
    
    vectorizer = TfidfVectorizer(max_features=maxx_features)
    X = vectorizer.fit_transform(text)
    return X
text = df['processed_desc'].values
X = vectorize(text, 2 ** 12) #arbitrary max feature -_> Hyperpara. for optimisation (?)
X.shape

from sklearn.decomposition import PCA

pca = PCA(n_components=0.95, random_state=42) #Keep 95% of the variance
X_reduced= pca.fit_transform(X.toarray())
X_reduced.shape




from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from scipy.spatial.distance import cdist
from sklearn import metrics
# find optimal k value
r_seed = 24
cluster_errors = []

for i in range(1, 75):
    n_clusters = i
    pipe_pca_kmean = Pipeline([("cluster", KMeans(n_clusters=n_clusters, random_state=r_seed, verbose=0))])

    pipe_pca_kmean.fit(X_reduced)
    pipe_pca_kmean.predict(X_reduced)
    cluster_errors.append(pipe_pca_kmean.named_steps["cluster"].inertia_) 

plt.clf()
plt.plot(cluster_errors, "o-")
plt.xlabel("k_clusters")
plt.ylabel("sum sq distances from mean")
plt.show()
plt.savefig('n_clusters_75_errors.png')

k =9 # optimal k found in elbow plot
kmeans = KMeans(n_clusters=k, random_state=42)
y_pred = kmeans.fit_predict(X_reduced)
df['kmean_clusters'] = y_pred


from sklearn.manifold import TSNE

tsne = TSNE(verbose=1, perplexity=100, random_state=42)
X_embedded = tsne.fit_transform(X.toarray())

import seaborn as sns

# sns settings
sns.set(rc={'figure.figsize':(15,15)})

# colors
palette = sns.color_palette("bright", 1)

# plot
sns.scatterplot(x=X_embedded[:,0], y=X_embedded[:,1], palette=palette)
plt.title('t-SNE without Labels')
plt.savefig("t-sne_arxvid.png")
plt.show()

%matplotlib inline

# sns settings
sns.set(rc={'figure.figsize':(15,15)})

# colors
palette = sns.hls_palette(20, l=.4, s=.9)

# plot
sns.scatterplot(x=X_embedded[:,0], y=X_embedded[:,1], hue=y_pred)
plt.title('t-SNE with Kmeans Labels')
plt.savefig("cluster_tsne.png")
plt.show()

left_acc,center_acc,right_acc=0,0,0
left_mis,center_mis,right_mis=0,0,0

for pred,bias in zip(df['kmean_clusters'],df['bias_id']):
	pred,bias=int(pred),int(bias)
	if bias <3:
		if pred<5:
			left_acc+=1
		else:
			left_mis+=1
	if bias >3:
		if pred>5:
			right_acc+=1
		else:
			right_mis+=1
	if bias==3:
		if pred==5:
			center+=1
		else:
			center_mis+=1

import plotly.express as px
fig = px.scatter(df, x=X_embedded[:,0], y=X_embedded[:,1], color=y_pred.astype(str),
                 hover_data=['id', 'authors', 'title'],
                 height= 1000, width=1000,
                title = "t-SNE with Kmeans Labels")
fig.show()

for 
# def import_allsides_data(dirname=r"/Users/greysonnewton/Desktop/txt-spch/youtube/allsides_data/"):
# 	ext = ('.csv')
# 	dfs=[]
# 	# iterating over all files
# 	for file in os.listdir(dirname):
# 	    if file.endswith(ext):
# 	        dfs.append(pd.read_csv(file))  # printing file name of desired extension
# 	    else:
# 	        continue	
# 	print('political data imported: ',len(dfs))
# 	return dfs
# def remove_noise(tweet_tokens, stop_words = ()):

#     cleaned_tokens = []

#     for token, tag in pos_tag(tweet_tokens):
#         token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
#                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
#         token = re.sub("(@[A-Za-z0-9_]+)","", token)

#         if tag.startswith("NN"):
#             pos = 'n'
#         elif tag.startswith('VB'):
#             pos = 'v'
#         else:
#             pos = 'a'

#         lemmatizer = WordNetLemmatizer()
#         token = lemmatizer.lemmatize(token, pos)

#         if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
#             cleaned_tokens.append(token.lower())
#     return cleaned_tokens
# def get_all_words(cleaned_tokens_list):
#     for tokens in cleaned_tokens_list:
#         for token in tokens:
#             yield token
# def get_tweets_for_model(cleaned_tokens_list):
#     for tweet_tokens in cleaned_tokens_list:
#         yield dict([token, True] for token in tweet_tokens)

# if __name__ == "__main__":

#     positive_tweets = twitter_samples.strings('positive_tweets.json')
#     negative_tweets = twitter_samples.strings('negative_tweets.json')
#     text = twitter_samples.strings('tweets.20150430-223406.json')
#     tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

#     stop_words = stopwords.words('english')

#     positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
#     negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

#     positive_cleaned_tokens_list = []
#     negative_cleaned_tokens_list = []

#     for tokens in positive_tweet_tokens:
#         positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

#     for tokens in negative_tweet_tokens:
#         negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

#     all_pos_words = get_all_words(positive_cleaned_tokens_list)

#     freq_dist_pos = FreqDist(all_pos_words)
#     print(freq_dist_pos.most_common(10))

#     positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
#     negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

#     positive_dataset = [(tweet_dict, "Positive")
#                          for tweet_dict in positive_tokens_for_model]

#     negative_dataset = [(tweet_dict, "Negative")
#                          for tweet_dict in negative_tokens_for_model]

#     dataset = positive_dataset + negative_dataset

#     random.shuffle(dataset)

#     train_data = dataset[:7000]
#     test_data = dataset[7000:]

#     classifier = NaiveBayesClassifier.train(train_data)

#     print("Accuracy is:", classify.accuracy(classifier, test_data))

#     print(classifier.show_most_informative_features(10))

#     # data=import_allsides_data()
#     # for df in data:
#     #     print(df.head())
#     # all_df,right_df,center_df,left_df=data[0],data[1],data[2],data[3]
#     all_df=pd.read_pickle("/Users/greysonnewton/Desktop/txt-spch/youtube/allsides_data/breaking_news.pkl")
#     sentiment=[]
#     sentiment_features=[]
#     for description in all_df['desc.']:
#         desc_tokens=remove_noise(word_tokenize(description))
#         results = classifier.classify(dict([token, True] for token in desc_tokens))
#         print(description,results)
#         sentiment.append(results)
        
#     all_df['nlp sentiment']=sentiment
#     all_df.to_csv('./allsides_data/breaking_news_sentiment.csv')
#     song = "done.mp3"    
#     playsound.playsound(song)