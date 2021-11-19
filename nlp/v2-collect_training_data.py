import re, csv, os
from time import sleep, time
from random import uniform, randint
import requests
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
cwd = os.getcwd()

# SAVES REQUESTS SAVES REQUESTS SAVES REQUESTS SAVES REQUESTS SAVES REQUESTS
reg_news_url = "https://www.allsides.com/topics-issues"
regular_news_links,regular_news_topics = [],[]
response = requests.get(reg_news_url)
soup = BeautifulSoup(response.text, "html.parser")
target = soup.find('div', class_='row-fluid normal-body').find_all('a')
regular_news_soups=[]
link = 'https://www.allsides.com/'
for a in target:
	# print(a)
	regular_news_links.append(a.get('href'))
	regular_news_topics.append(a.text)
regular_news_links = [link + l for l in regular_news_links]
regular_news_links = [l.replace(" ","") for l in regular_news_links]
print(regular_news_links)
print('getting requests')
regular_news_links=regular_news_links
for i,l in enumerate(regular_news_links):
	res = requests.get(l)
	regular_news_soups.append(BeautifulSoup(res.text, "html.parser"))
print('saved requests')
# print('opening requests')
# for file in os.listdir("/Users/greysonnewton/Desktop/txt-spch/youtube/youtube_ai/nlp/requests"):
# 	if file.endswith(".html"):
# 		fname=os.path.join("/Users/greysonnewton/Desktop/txt-spch/youtube/youtube_ai/nlp/requests", file)
# 		with open(fname) as f:
# 			soup = BeautifulSoup(f,"html.parser")
# 			regular_news_soups.append(soup)
print('soupified requests')
topic_grid_selector='#elections-wrapper > div:nth-child(5) > div.region.region-global-news-trio'
#block-views-balanced-news-trio-block-2 > div > div > div
# print(regular_news_soups)
l_news,r_news,c_news,a_news=[],[],[],[]
r_topics,r_topic_ids,r_types,r_links,r_titles,r_descs,r_srcs,r_biases,r_bias_ids,r_imgs=[],[],[],[],[],[],[],[],[],[]
l_topics,l_topic_ids,l_types,l_links,l_titles,l_descs,l_srcs,l_biases,l_bias_ids,l_imgs=[],[],[],[],[],[],[],[],[],[]
c_topics,c_topic_ids,c_types,c_links,c_titles,c_descs,c_srcs,c_biases,c_bias_ids,c_imgs=[],[],[],[],[],[],[],[],[],[]
#block-views-balanced-news-trio-block-2 > div > div > div
for i,s in enumerate(regular_news_soups):
	topic_grid=s.find_all("div",{"class":"news-trio"})
	print('getting news from, ',regular_news_topics[i])	
	# print(topic_grid)
	# handle=topic_grid[0]
	l_items=s.find_all("div",{"class":"news-item left"})
	r_items=s.find_all("div",{"class":"news-item right"})
	c_items=s.find_all("div",{"class":"news-item center"})
	# print(l_items)
	# print(l_items[0])
	for e,item in enumerate(l_items):
		news_type=item.find("div",{"class":"news-type-label"})
		if news_type!=None:
			news_type=news_type.text.strip()
		else:
			news_type='n/a'
		link=item.find('a')
		if link!= None:
			link=link.get('href')
		else:
			link='n/a'
		title=item.find('a').find('div')
		if title!= None:
			title=title.text.strip()
		else:
			title='n/a'
		src=item.find("div",{"class":"news-source"})
		if src != None:
			src=src.text.strip()
		else:
			src='n/a'
		bias=item.find("a",{"class":"source-area"}).find('img')
		if bias != None:
			bias=bias.get('title').split(':',1)[1].strip()
		else:
			bias='n/a'
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
		desc=bs.find("div",{"class":"article-description"})
		if desc != None:
			desc=desc.text.strip()
		else:
			desc='n/a'
		img=bs.select('#block-views-article-page-redesign-block-1 > div > div.view-content > div > div.article-page-detail > div.second-portion > div.span8 > div.article-image > div > img')
		fname='n/a'
		if img == None or len(img)==0:
			fname='n/a'
		else:
			link=img[0].get('src')
			if 'jpg' in link:
				ext='.jpg'
				fname=cwd+'/data/allsides_training_data/images/'+regular_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
								
			elif 'png' in link:
				ext='.png'
				fname=cwd+'/data/allsides_training_data/images/'+regular_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
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
			l_topics.append(regular_news_topics[i])
			l_topic_ids.append(i)


	for e,item in enumerate(r_items):
		news_type=item.find("div",{"class":"news-type-label"})
		if news_type!=None:
			news_type=news_type.text.strip()
		else:
			news_type='n/a'
		link=item.find('a')
		if link!= None:
			link=link.get('href')
		else:
			link='n/a'
		title=item.find('a').find('div')
		if title!= None:
			title=title.text.strip()
		else:
			title='n/a'
		src=item.find("div",{"class":"news-source"})
		if src != None:
			src=src.text.strip()
		else:
			src='n/a'
		bias=item.find("a",{"class":"source-area"}).find('img')
		if bias != None:
			bias=bias.get('title').split(':',1)[1].strip()
		else:
			bias='n/a'
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
		desc=bs.find("div",{"class":"article-description"})
		if desc != None:
			desc=desc.text.strip()
		else:
			desc='n/a'
		img=bs.select('#block-views-article-page-redesign-block-1 > div > div.view-content > div > div.article-page-detail > div.second-portion > div.span8 > div.article-image > div > img')
		if img == None or len(img)==0:
			fname='n/a'
		else:
			link=img[0].get('src')
			if 'jpg' in link:
				ext='.jpg'
				fname=cwd+'/data/allsides_training_data/images/'+regular_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
			elif 'png' in link:
				ext='.png'
				fname=cwd+'/data/allsides_training_data/images/'+regular_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
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
			r_topics.append(regular_news_topics[i])
			r_topic_ids.append(i)

	for e,item in enumerate(c_items):
		news_type=item.find("div",{"class":"news-type-label"})
		if news_type!=None:
			news_type=news_type.text.strip()
		else:
			news_type='n/a'
		link=item.find('a')
		if link!= None:
			link=link.get('href')
		else:
			link='n/a'
		title=item.find('a').find('div')
		if title!= None:
			title=title.text.strip()
		else:
			title='n/a'
		src=item.find("div",{"class":"news-source"})
		if src != None:
			src=src.text.strip()
		else:
			src='n/a'
		bias=item.find("a",{"class":"source-area"}).find('img')
		if bias != None:
			bias=bias.get('title').split(':',1)[1].strip()
		else:
			bias='n/a'
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
		desc=bs.find("div",{"class":"article-description"})
		if desc != None:
			desc=desc.text.strip()
		else:
			desc='n/a'
		img=bs.select('#block-views-article-page-redesign-block-1 > div > div.view-content > div > div.article-page-detail > div.second-portion > div.span8 > div.article-image > div > img')
		if img == None or len(img)==0:
			fname='n/a'
		else:
			link=img[0].get('src')
			if 'jpg' in link:
				ext='.jpg'
				fname=cwd+'/data/allsides_training_data/images/'+regular_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
				with open(fname, "wb") as f:
					f.write(requests.get(link).content)
			elif 'png' in link:
				ext='.png'
				fname=cwd+'/data/allsides_training_data/images/'+regular_news_topics[i]+str(bias_id)+'itemnum'+str(e)+ext
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
			c_topics.append(regular_news_topics[i])
			c_topic_ids.append(i)

fname="/Users/greysonnewton/Desktop/txt-spch/youtube/youtube_ai/nlp/data/allsides_training_data/"

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