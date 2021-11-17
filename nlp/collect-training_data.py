import re, csv, os
from time import sleep, time
from random import uniform, randint
import requests
import urllib.request
from urllib.request import urlopen

from bs4 import BeautifulSoup
import pandas as pd

# SAVES REQUESTS SAVES REQUESTS SAVES REQUESTS SAVES REQUESTS SAVES REQUESTS
reg_news_url = "https://www.allsides.com/topics-issues"
regular_news_links,regular_news_topics = [],[]
response = requests.get(reg_news_url)
soup = BeautifulSoup(response.text, "html.parser")
target = soup.find('div', class_='row-fluid normal-body').find_all('a')

link = 'https://www.allsides.com/'
for a in target:
	# print(a)
	regular_news_links.append(a.get('href'))
	regular_news_topics.append(a.text)

# regular_news_links = [link + l for l in regular_news_links]
# regular_news_links = [l.replace(" ","") for l in regular_news_links]
# # print(regular_news_links)
# print('getting requests')
# for i,l in enumerate(regular_news_links):
# 	res = urlopen(l)
# 	fname="/Users/greysonnewton/Desktop/txt-spch/youtube/requests/"+str(i)+"_soup.html"
# 	with open(fname, "wb") as f:
# 		while True:
# 			chunk = res.read(1024)
# 			if not chunk:
# 				break
# 			f.write(chunk)
# 	# regular_news_soups.append(BeautifulSoup(res.text, "html.parser"))
# print('saved requests')

regular_news_soups = []
print('opening requests')
for file in os.listdir("/Users/greysonnewton/Desktop/txt-spch/youtube/requests/"):
	if file.endswith(".html"):
		fname=os.path.join("/Users/greysonnewton/Desktop/txt-spch/youtube/requests/", file)
		with open(fname) as f:
			soup = BeautifulSoup(f)
			regular_news_soups.append(soup)
print('soupified requests')

def get_data(soups,regular_news_topics):
	df = pd.DataFrame()
	page_titles = []
	page_descriptions=[]
	left_news,center_news,right_news=[],[],[]


	left_titles,center_titles,right_titles = [],[],[]
	left_descs,center_descs,right_descs = [],[],[]
	left_src,center_src,right_src = [],[],[]
	left_bias,center_bias,right_bias = [],[],[]
	left_topics,right_topics,center_topics=[],[],[]
	left_topics_id,right_topics_id,center_topics_id=[],[],[]
	left_bias_id,center_bias_id,right_bias_id = [],[],[]
	for i,s in enumerate(soups):
		tag=False
		# page_title = s.find("div", {"class": "span12"}).find("h1")
		# if page_title != None:
		# 	page_titles.append(page_title.text)
		# else:
		# 	page_title = s.select('#blog-wrapper > div:nth-child(1) > div > h2')
		# 	if page_title != None:
		# 		page_titles.append(page_title[0].text)
		# 	else:
		# 		page_titles.append('page title not found')
	
		# page_description = s.find("div", {"class": "span12"}).find("div", {"class": "span12 topic-description"})
		# if page_description == None:
		# 	page_descriptions.append('tag seach, no desc.')
		# else:
		# 	page_descriptions.append(page_description.text)


		not_found='news not found'
		
		

		# checking for tag:
		tag=s.select('#main > h1')
		# topic=s.selct('#block-views-elections-topic-block-4 > div > div > div > div > div:nth-child(3) > div > div > h1')
		# checking for news grid
		if tag != None:
			# print(tag)
			if len(tag)>=1:
				print(regular_news_topics[i], 'is a tag')
				left_news_selector='#block-views-news-trio-tag-block > h2'
				left_grid_selector='#block-views-news-trio-tag-block > div'				
				right_news_selector='#block-views-news-trio-tag-block-2 > h2'
				right_grid_selector='#block-views-news-trio-tag-block-2 > div'
				center_news_selector='#block-views-news-trio-tag-block-3 > h2'
				center_grid_selector='#block-views-news-trio-tag-block-3 > div'
				tag=True
			elif len(tag)==0:
				print(regular_news_topics[i], 'is a topic')
				left_news_selector='#block-views-news-trio-topic-block > h2'
				left_grid_selector='#block-views-news-trio-topic-block > div'
				right_news_selector='#block-views-news-trio-topic-block-2 > h2'
				right_grid_selector='#block-views-news-trio-topic-block-2 > div'
				center_news_selector='#block-views-news-trio-topic-block-1 > h2'
				center_grid_selector='#block-views-news-trio-topic-block-1 > div'
				#block-views-news-trio-topic-block-1			
		# checking for existence
		news_from_left = s.select(left_news_selector)
		if news_from_left != None and len(news_from_left)>=1:
			left_news.append(news_from_left[0].text)
		else:
			left_news.append(not_found)
			print(regular_news_topics[i], 'not found')
		# getting news from column
		left_news_grid_handle=s.select(left_grid_selector)
		if left_news_grid_handle != None and len(left_news_grid_handle)>=1:
			left_grid=left_news_grid_handle[0]
			for news_title in left_grid.find_all("div", {"class": "news-title"}):
				# print(news_title.find('a').text)
				left_titles.append(news_title.find('a').text)
				
			for news_description in left_grid.find_all("div", {"class": "topic-description"}):
				# print(news_description.find('p').text)
				left_descs.append(news_description.find('p').text)
			for news_bias in left_grid.find_all("div", {"class": "source-area"}):
				news_source=news_bias.find('div',{'class':'news-source'})
				# print(news_source.find('a').text)
				bias=news_bias.find('div',{'class':'bias-container'})
				# print(bias.find('div',{'class':'field-content'}).find('img').get('title').split(':',1)[1])
				left_src.append(news_source.find('a').text)
				left_bias.append(bias.find('img').get('title').split(':',1)[1])
				topic=regular_news_topics[i]+'-'+bias.find('img').get('title').split(':',1)[1]
				left_topics.append(topic)
				left_topics_id.append(i+1)
				# print(news_bias.find('a').text)
				# print(news_bias.find("div", {"class": "field-content"}))				
				if 'Lean' in left_bias[-1]:
					left_bias_id.append('1')
				elif not('Lean' in left_bias[-1]):
					left_bias_id.append('2')
		# checking existence
		news_from_right = s.select(right_news_selector)
		if news_from_right != None and len(news_from_right)>=1:
			right_news.append(news_from_right[0].text)
		else:
			right_news.append(not_found)
			print(regular_news_topics[i], 'not found')

		# getting news
		right_news_grid_handle=s.select(right_grid_selector)
		if right_news_grid_handle != None and len(right_news_grid_handle)>=1:
			right_grid=right_news_grid_handle[0]
			for news_title in right_grid.find_all("div", {"class": "news-title"}):
				# print(news_title.find('a').text)
				right_titles.append(news_title.find('a').text)
			for news_description in right_grid.find_all("div", {"class": "topic-description"}):
				# print(news_description.find('p').text)
				right_descs.append(news_description.find('p').text)
			for news_bias in right_grid.find_all("div", {"class": "source-area"}):
				news_source=news_bias.find('div',{'class':'news-source'})
				# print(news_source.find('a').text)
				bias=news_bias.find('div',{'class':'bias-container'})
				# print(bias.find('div',{'class':'field-content'}).find('img').get('title').split(':',1)[1])
				right_src.append(news_source.find('a').text)
				right_bias.append(bias.find('img').get('title').split(':',1)[1])
				# print(news_bias.find('a').text)
				# print(news_bias.find("div", {"class": "field-content"}))	
				topic=regular_news_topics[i]+'-'+bias.find('img').get('title').split(':',1)[1]
				right_topics.append(topic)
				right_topics_id.append(i+1)
				if 'Lean' in right_bias[-1]:
					right_bias_id.append('4')
				elif not('Lean' in right_bias[-1]):
					right_bias_id.append('5')
		# checking existence
		news_from_center = s.select(center_news_selector)
		if news_from_center != None and len(news_from_center)>=1:
			center_news.append(news_from_center[0].text)
		else:
			center_news.append(not_found)
			print(regular_news_topics[i], 'not found')

		# getting news
		center_news_grid_handle=s.select(center_grid_selector)
		if center_news_grid_handle != None and len(center_news_grid_handle)>=1:
			center_grid=center_news_grid_handle[0]
			for news_title in center_grid.find_all("div", {"class": "news-title"}):
				# print(news_title.find('a').text)
				center_titles.append(news_title.find('a').text)
			for news_description in center_grid.find_all("div", {"class": "topic-description"}):
				# print(news_description.find('p').text)
				center_descs.append(news_description.find('p').text)
			for news_bias in center_grid.find_all("div", {"class": "source-area"}):
				news_source=news_bias.find('div',{'class':'news-source'})
				# print(news_source.find('a').text)
				bias=news_bias.find('div',{'class':'bias-container'})
				# print(bias.find('div',{'class':'field-content'}).find('img').get('title').split(':',1)[1])
				center_src.append(news_source.find('a').text)
				center_bias.append('moderate')
				topic=regular_news_topics[i]+' -'+' moderate'
				center_topics.append(topic)
				center_topics_id.append(i+1)
				center_bias_id.append('3')
				# print(news_bias.find('a').text)
				# print(news_bias.find("div", {"class": "field-content"}))	
	# for title,description,source,bias in zip(left_titles,left_descs,left_src,left_bias):
	# 	print(title.strip(),'\t',source.strip(),'\t',bias.strip(),'\n',description.strip(),'\n')
	left_df,right_df,center_df=pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
	left_df['topic_id']=left_topics_id
	left_df['bias_id']=left_bias_id
	left_df['topic']=left_topics
	left_df['title']=left_titles
	left_df['source']=left_src
	left_df['bias']=left_bias

	left_df['desc.']=left_descs
	left_df.to_csv('./allsides_training_data/left_breaking_news.csv', index=False)
	left_df.to_pickle("./allsides_training_data/left_breaking_news.pkl")

	right_df['topic_id']=right_topics_id
	right_df['bias_id']=right_bias_id
	right_df['topic']=right_topics
	right_df['title']=right_titles
	right_df['source']=right_src
	right_df['bias']=right_bias
	right_df['desc.']=right_descs
	right_df.to_csv('./allsides_training_data/right_breaking_news.csv', index=False)
	right_df.to_pickle("./allsides_training_data/right_breaking_news.pkl")

	center_df['topic_id']=center_topics_id
	center_df['bias_id']=center_bias_id
	center_df['topic']=center_topics
	center_df['title']=center_titles
	center_df['source']=center_src
	center_df['bias']=center_bias
	center_df['desc.']=center_descs
	center_df.to_csv('./allsides_training_data/center_breaking_news.csv', index=False)
	center_df.to_pickle("./allsides_training_data/center_breaking_news.pkl")

	topics,topics_id,bias_id,titles,srcs,biases,descs = [],[],[],[],[],[],[]
	for left,center,right in zip(left_topics,right_topics,center_topics):
		topics.append(left)
		topics.append(center)
		topics.append(right)
	print('len of topics',len(topics))		
	for left,center,right in zip(left_topics_id,right_topics_id,center_topics_id):
		topics_id.append(left)
		topics_id.append(center)
		topics_id.append(right)
	print('len of topic ids',len(topics_id))
	for left,center,right in zip(left_bias_id,right_bias_id,center_bias_id):
		bias_id.append(left)
		bias_id.append(center)
		bias_id.append(right)
	print('len of biases',len(bias_id))						
	for left,center,right in zip(left_titles,right_titles,center_titles):
		titles.append(left)
		titles.append(center)
		titles.append(right)
	for left,center,right in zip(left_src,right_src,center_src):
		srcs.append(left)
		srcs.append(center)
		srcs.append(right)
	for left,center,right in zip(left_bias,right_bias,center_bias):
		biases.append(left)
		biases.append(center)
		biases.append(right)
	for left,center,right in zip(left_descs,right_descs,center_descs):
		descs.append(left)
		descs.append(center)
		descs.append(right)
	df['topic']=topics
	df['topic_id']=topics_id
	df['bias_id']=bias_id
	df['title']=titles
	df['source']=srcs
	df['bias']=biases
	df['desc.']=descs
	print(topics_id)
	df.to_csv('./allsides_training_data/breaking_news.csv', index=False)
	df.to_pickle("./allsides_training_data/breaking_news.pkl")

	return df

print('getting data')
data = get_data(regular_news_soups,regular_news_topics)
print('got data')
print(data.head())