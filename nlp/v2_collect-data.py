import re, csv, os
from time import sleep, time
from random import uniform, randint
import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import pickle
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
from os.path  import basename
cwd = os.getcwd()
		
		# item = [topic,topic_id,news_type,title,desc,src,bias,bias_id,link,l_imgs[-1]]
		# items.append(item)
	# print(types)
# def save_news(l_news,r_news,c_news,a_news):
# 	print('saving news')
# 	features=['topics','topic_ids','types','titles','descs','srcs','biases','bias_ids','links','imgs']
	
# 	l_fname=cwd+'/data/allsides_data/l_breaking_news.csv'
# 	l_df=pd.DataFrame()
# 	for topic in l_news:
# 		print('topic',topic[0],len(topic))
# 		for f,feature in zip(features,topic):
# 			print('feature',feature[0],len(feature))
# 			l_df[f]=feature
# 	l_df.to_csv(l_fname)
# 	print('saved to l_breaking_news.csv')

# 	r_fname=cwd+'/data/allsides_data/r_breaking_news.csv'
# 	r_df=pd.DataFrame()
# 	for topic in r_news:
# 		for f,feature in zip(features,topic):
# 			r_df[f]=feature
# 	r_df.to_csv(r_fname)
# 	print('saved to r_breaking_news.csv')

# 	c_fname=cwd+'/data/allsides_data/c_breaking_news.csv'
# 	c_df=pd.DataFrame()
# 	for topic in c_news:
# 		for f,feature in zip(features,topic):
# 			c_df[f]=feature
# 	c_df.to_csv(c_fname)
# 	print('saved to c_breaking_news.csv')
																	
# 	all_fname=cwd+'/data/allsides_data/all_breaking_news.csv'
# 	all_df = pd.DataFrame()
# 	for topic in all_news:
# 		for f,feature in zip(features,topic):
# 			all_df[f]=feature
# 	all_df.to_csv(all_fname)
# 	print('saved to all_breaking_news.csv')
# 	print('-finished saving news-')
	
url = "https://www.allsides.com/unbiased-balanced-news"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
target = soup.find('div', class_='breaking-news').find('ul').find_all('a')
# Get news topics
print('-Getting breaking news topics-')
link = 'https://www.allsides.com/'
breaking_news_links = []
for a in target:
	breaking_news_links.append(a['href'])
breaking_news_links = [link + l for l in breaking_news_links]
breaking_news_topics=[l.rsplit('/',1)[1] for l in breaking_news_links]
print('topics ',breaking_news_topics)
print('-souping breaking news topics-')
soups = []
for l in breaking_news_links:
	res = requests.get(l)
	soups.append(BeautifulSoup(res.text, "html.parser"))
print('-souped breaking news topics-')
topic_grid_selector='#block-views-balanced-news-trio-block-2 > div > div > div'
print('-Getting breaking news items-')
l_news,r_news,c_news,a_news=[],[],[],[]
r_topics,r_topic_ids,r_types,r_links,r_titles,r_descs,r_srcs,r_biases,r_bias_ids,r_imgs=[],[],[],[],[],[],[],[],[],[]
l_topics,l_topic_ids,l_types,l_links,l_titles,l_descs,l_srcs,l_biases,l_bias_ids,l_imgs=[],[],[],[],[],[],[],[],[],[]
c_topics,c_topic_ids,c_types,c_links,c_titles,c_descs,c_srcs,c_biases,c_bias_ids,c_imgs=[],[],[],[],[],[],[],[],[],[]

for i,s in enumerate(soups):

	print('getting news from, ',breaking_news_topics[i])	
	topic_grid=s.select(topic_grid_selector)
	handle=topic_grid[0]
	l_items=handle.find_all("div",{"class":"news-item left"})
	r_items=handle.find_all("div",{"class":"news-item right"})
	c_items=handle.find_all("div",{"class":"news-item center"})
	# print(l_items[0])
	for e,item in enumerate(l_items):
		news_type=item.find("div",{"class":"news-type-label"}).text.strip()
		link=item.find('a').get('href')
		title=item.find('a').find('div').text.strip()
		src=item.find("div",{"class":"news-source"}).text.strip()
		bias=item.find("a",{"class":"source-area"}).find('img').get('title').split(':',1)[1].strip()
		if not('Lean' in bias) and 'Left' in bias:
			bias_id=1
		if 'Lean Left' in bias:
			bias_id=2
		if 'Center' in bias:
			bias_id=2
		if 'Lean Right' in bias:
			bias_id=4
		if not('Lean' in bias) and 'Right' in bias:
			bias_id=5
		l=requests.get(link)
		bs = BeautifulSoup(l.text, "html.parser")
		desc=bs.find("div",{"class":"article-description"}).text.strip()
		img=bs.select('#block-views-article-page-redesign-block-1 > div > div.view-content > div > div.article-page-detail > div.second-portion > div.span8 > div.article-image > div > img')
		if img == None or len(img)==0:
			fname='n/a'
		else:
			link=img[0].get('src')
			if 'jpg' in link:
				ext='.jpg'
				fname=cwd+'/data/allsides_data/images/'+breaking_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
								
			elif 'png' in link:
				ext='.png'
				fname=cwd+'/data/allsides_data/images/'+breaking_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
			l_imgs.append(fname)
			l_types.append(news_type)
			l_links.append(link)
			l_titles.append(title)
			l_descs.append(desc)
			l_srcs.append(src)
			l_biases.append(bias)
			l_bias_ids.append(bias_id)
			l_topics.append(breaking_news_topics[i])
			l_topic_ids.append(i)


	for e,item in enumerate(r_items):
		news_type=item.find("div",{"class":"news-type-label"}).text.strip()
		link=item.find('a').get('href')
		title=item.find('a').find('div').text.strip()
		src=item.find("div",{"class":"news-source"}).text.strip()
		bias=item.find("a",{"class":"source-area"}).find('img').get('title').split(':',1)[1].strip()
		if not('Lean' in bias) and 'Left' in bias:
			bias_id=1
		if 'Lean Left' in bias:
			bias_id=2
		if 'Center' in bias:
			bias_id=2
		if 'Lean Right' in bias:
			bias_id=4
		if not('Lean' in bias) and 'Right' in bias:
			bias_id=5
		l=requests.get(link)
		bs = BeautifulSoup(l.text, "html.parser")
		desc=bs.find("div",{"class":"article-description"}).text.strip()
		img=bs.select('#block-views-article-page-redesign-block-1 > div > div.view-content > div > div.article-page-detail > div.second-portion > div.span8 > div.article-image > div > img')
		if img == None or len(img)==0:
			fname='n/a'
		else:
			link=img[0].get('src')
			if 'jpg' in link:
				ext='.jpg'
				fname=cwd+'/data/allsides_data/images/'+breaking_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
			elif 'png' in link:
				ext='.png'
				fname=cwd+'/data/allsides_data/images/'+breaking_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
			r_imgs.append(fname)
			r_types.append(news_type)
			r_links.append(link)
			r_titles.append(title)
			r_descs.append(desc)
			r_srcs.append(src)
			r_biases.append(bias)
			r_bias_ids.append(bias_id)
			r_topics.append(breaking_news_topics[i])
			r_topic_ids.append(i)

	for e,item in enumerate(c_items):
		news_type=item.find("div",{"class":"news-type-label"}).text.strip()
		link=item.find('a').get('href')
		title=item.find('a').find('div').text.strip()
		src=item.find("div",{"class":"news-source"}).text.strip()
		bias=item.find("a",{"class":"source-area"}).find('img').get('title').split(':',1)[1].strip()
		if not('Lean' in bias) and 'Left' in bias:
			bias_id=1
		if 'Lean Left' in bias:
			bias_id=2
		if 'Center' in bias:
			bias_id=2
		if 'Lean Right' in bias:
			bias_id=4
		if not('Lean' in bias) and 'Right' in bias:
			bias_id=5
		l=requests.get(link)
		bs = BeautifulSoup(l.text, "html.parser")
		desc=bs.find("div",{"class":"article-description"}).text.strip()
		img=bs.select('#block-views-article-page-redesign-block-1 > div > div.view-content > div > div.article-page-detail > div.second-portion > div.span8 > div.article-image > div > img')
		if img == None or len(img)==0:
			fname='n/a'
		else:
			link=img[0].get('src')
			if 'jpg' in link:
				ext='.jpg'
				fname=cwd+'/data/allsides_data/images/'+breaking_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
			elif 'png' in link:
				ext='.png'
				fname=cwd+'/data/allsides_data/images/'+breaking_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
			c_imgs.append(fname)
			c_types.append(news_type)
			c_links.append(link)
			c_titles.append(title)
			c_descs.append(desc)
			c_srcs.append(src)
			c_biases.append(bias)
			c_bias_ids.append(bias_id)
			c_topics.append(breaking_news_topics[i])
			c_topic_ids.append(i)

fname="/Users/greysonnewton/Desktop/txt-spch/youtube/youtube_ai/nlp/data/allsides_data/"

l_df,r_df,c_df,all_df=pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()

print(len(l_topic_ids),len(l_topics),len(l_bias_ids),len(l_types),len(l_titles),len(l_descs),len(l_srcs),len(l_biases),len(l_links),len(l_imgs))

l_df['topic_id']=l_topic_ids
l_df['topic']=l_topics
l_df['bias_id']=l_bias_ids
l_df['type']=l_types
l_df['title']=l_titles
l_df['desc']=l_descs
l_df['src']=l_srcs
l_df['bias']=l_biases
l_df['link']=l_links
l_df['link']=l_imgs

r_df['topic_id']=r_topic_ids
r_df['topic']=r_topics
r_df['bias_id']=r_bias_ids
r_df['type']=r_types
r_df['title']=r_titles
r_df['desc']=r_descs
r_df['src']=r_srcs
r_df['bias']=r_biases
r_df['link']=r_links
r_df['link']=r_imgs	

c_df['topic_id']=c_topic_ids
c_df['topic']=c_topics
c_df['bias_id']=c_bias_ids
c_df['type']=c_types
c_df['title']=c_titles
c_df['desc']=c_descs
c_df['src']=c_srcs
c_df['bias']=c_biases
c_df['link']=c_links
c_df['link']=c_imgs

topics,topic_ids,bias_id,types,titles,srcs,biases,descs,links,imgs = [],[],[],[],[],[],[],[],[],[]
for left,center,right in zip(l_topic_ids,r_topic_ids,c_topic_ids):
	topic_ids.append(left)
	topic_ids.append(center)
	topic_ids.append(right)
print('len of topic ids',len(topic_ids))
for left,center,right in zip(l_topics,r_topics,c_topics):
	topics.append(left)
	topics.append(center)
	topics.append(right)
print('len of topics',len(topics))		
for left,center,right in zip(l_bias_ids,r_bias_ids,c_bias_ids):
	bias_id.append(left)
	bias_id.append(center)
	bias_id.append(right)
print('len of biases',len(bias_id))	
for left,center,right in zip(l_types,r_types,c_types):
	types.append(left)
	types.append(center)
	types.append(right)						
for left,center,right in zip(l_titles,r_titles,c_titles):
	titles.append(left)
	titles.append(center)
	titles.append(right)
for left,center,right in zip(l_descs,r_descs,c_descs):
	descs.append(left)
	descs.append(center)
	descs.append(right)		
for left,center,right in zip(l_srcs,r_srcs,c_srcs):
	srcs.append(left)
	srcs.append(center)
	srcs.append(right)
for left,center,right in zip(l_biases,r_biases,c_biases):
	biases.append(left)
	biases.append(center)
	biases.append(right)
for left,center,right in zip(l_links,r_links,c_links):
	links.append(left)
	links.append(center)
	links.append(right)
for left,center,right in zip(l_imgs,r_imgs,c_imgs):
	imgs.append(left)
	imgs.append(center)
	imgs.append(right)	


all_df['topic_id']=topic_ids
all_df['topic']=topics
all_df['bias_id']=bias_id
all_df['type']=types
all_df['title']=titles
all_df['desc']=descs
all_df['src']=srcs
all_df['bias']=biases
all_df['link']=links
all_df['link']=imgs
l_df.to_csv(fname+"l_breaking_news.csv", index=False)
l_df.to_pickle(fname+"l_breaking_news.pkl")
r_df.to_csv(fname+"r_breaking_news.csv", index=False)
r_df.to_pickle(fname+"r_breaking_news.pkl")	
c_df.to_csv(fname+"c_breaking_news.csv", index=False)
c_df.to_pickle(fname+"c_breaking_news.pkl")	
all_df.to_csv(fname+"all_breaking_news.csv", index=False)
all_df.to_pickle(fname+"all_breaking_news.pkl")								
	


