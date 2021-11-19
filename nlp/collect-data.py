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
# For all - need to incorporate a mechanism that returns probability of similarity of information gathered from different sources -
#
#
# Climate bot : https://insideclimatenews.org
# 	-fox
# 	-msnbc
# 	-cnn
# Politic bot : https://www.allsides.com/unbiased-balanced-news
# 	-fox
# 	-msnbc
# 	-cnn
# Entertainment bot :
#
# Separate into Movies & TV, Music, General
#
# 	-cnn
# 	-cbs: https://www.cbsnews.com/entertainment/
# 	-etonline: https://www.etonline.com/news
# 	-today: https://www.today.com/popculture
#
# Discover new places bot :

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(ChromeDriverManager().install())
# # url -> xpath -> data -> images -> music -> video -> youtube -> sentiment analysis on comments 

# urls
l_articles, l_images = ["https://en.wikipedia.org/wiki/Cultural_area"],[]
l_places = [l_articles]
l_political, l_climate, l_entertainment = ["https://www.allsides.com/unbiased-balanced-news"], ["insideclimatenews.org"], ["https://www.cbsnews.com/entertainment/", "https://www.etonline.com/news", "https://www.today.com/popculture"]
l_current_events=["https://en.wikipedia.org/wiki/Portal:Current_events"]
l_headlines = [l_political, l_climate, l_entertainment, l_current_events]
# xpaths
x_articles, x_images = [], []
x_places = [x_articles, x_images]
x_political, x_climate, x_entertainment = [],[],[]
x_headlines = [x_political, x_climate, x_entertainment]
# [link],[culture,countries]
l_x_places = [["https://en.wikipedia.org/wiki/Cultural_area"],
["/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[1]/a",
"/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[1]/td[1]",
"/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[22]/td[1]"]]

# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[2]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[3]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[4]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[5]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[6]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[7]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[8]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[9]/a",
# "/html/body/div[3]/div[3]/div[5]/div[1]/ul[6]/li/ul/li[10]/a"]

# import sys
# import subprocess
# packagename='plotly'
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', packagename])
# target = soup.find('div',class_='breaking-news').find('ul').find_all('a')
# data
d_articles,d_images = [],[]
d_places = [d_articles,d_images]
d_political,d_climate,d_entertainment = [],[],[]
d_headlines = [d_political,d_climate,d_entertainment]

def gather_places():
	link = "https://en.wikipedia.org"
	url="https://en.wikipedia.org/wiki/Cultural_area"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	cultures=soup.findAll('ul')[15]
	print("----------cultures----------")
	cul_as=cultures.findAll('a')
	titles=[]
	for i in cul_as:
		print(i['title'])
		titles.append(i['title'])
	# print(cultures)
	# for c in cultures:
	# 	# li_child =c.findAll("li")
	# 	a=c.findChild('a')
	# 	print(a['title'])
		# if li_child !=None:
		# 	a_child=li_child.findChild("a")
		# 	print(a_child['title'])	
	country_links=[]
	for i in cul_as:
		country_links.append(i['href'])
	country_links=[link+c for c in country_links]
	print("----------country_links----------")
	print(country_links)
	soups=[]
	for url in country_links:
		response=requests.get(url)
		soup=BeautifulSoup(response.text,"html.parser")
		soups.append(soup)
	tables=[]
	print("----------tables----------")

	for s,culture in zip(soups,titles):
		table=s.find('table')
		tables.append(table)
		elements=[]
		if table !=None:
			child =table.findChild("th")
		
			if child != None and child.text != None and "Country" in child.text:
				country_child=table.findChild("tbody")
				print("  ----------CULTURE :",culture)
				if country_child != None:
					country_entries=country_child.findAll('a')
					# print(country_entries)
					for entry in country_entries:
						if entry.has_attr('title'):
							country_name=entry['title']
							print("\t----------table:",country_name)
	ofname="places_search_terms.txt"
# bbid.py [-h] [-s SEARCH_STRING] [-f SEARCH_FILE] [-o OUTPUT]
#                [--adult-filter-on] [--adult-filter-off] [--filters FILTERS]
#                [--limit LIMIT]

	
		# for ele in table:
			
		# 	if child != None and child.find("a"):
		# 		countries=child.find("a")
		# 		if countries.has_attr('title'):
		# 			print("\t",countries['title'])
			# if child != None:
			# 	if child.has_attr('title'):
			# 		print('title ',child['title'])
			# 	if child.has_attr('href'):
			# 		print('link ',child['href'])					
			# 	print(ele)	
			# print(type(ele))
# gather_places()

url = "https://www.allsides.com/unbiased-balanced-news"

def gather_political_news(url):

	# Get Allsides webpage
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	target = soup.find('div', class_='breaking-news').find('ul').find_all('a')

	# Get news topics
	link = 'https://www.allsides.com/'
	breaking_news_links = []
	for a in target:
		breaking_news_links.append(a['href'])
	breaking_news_links = [link + l for l in breaking_news_links]
	breaking_news_topics=[l.rsplit('/',1)[1] for l in breaking_news_links]
	print(breaking_news_topics)

	# get regular news for training data
	# reg_news_url = "https://www.allsides.com/topics-issues"
	# regular_news_links,regular_news_topics = [],[]
	# response = requests.get(reg_news_url)
	# soup = BeautifulSoup(response.text, "html.parser")
	# target = soup.find('div', class_='row-fluid normal-body').find_all('a')
	# for a in target:
	# 	regular_news_links.append(a['href'])
	# 	regular_news_topics.append(a['text'])
	# print(regular_news_topics)
	# Convert news topics to bs4
	soups = []
	for l in breaking_news_links:
		res = requests.get(l)
		soups.append(BeautifulSoup(res.text, "html.parser"))
	# news_content = soup.find_all("div", {"class": "view-content"})
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



		not_found='news not found'
		
		

		# checking for tag:
		tag=s.select('#main > h1')
		# topic=s.selct('#block-views-elections-topic-block-4 > div > div > div > div > div:nth-child(3) > div > div > h1')
		# checking for news grid
		if tag != None:
			# print(tag)
			if len(tag)>=1:
				print(breaking_news_topics[i], 'is a tag')
				left_news_selector='#block-views-news-trio-tag-block > h2'
				# left_grid_selector='#block-views-news-trio-tag-block > div'
				left_grid_selector='#block-views-news-trio-tag-block > div > div'				
				right_news_selector='#block-views-news-trio-tag-block-2 > h2'
				right_grid_selector='#block-views-news-trio-tag-block-2 > div'
				center_news_selector='#block-views-news-trio-tag-block-3 > h2'
				center_grid_selector='#block-views-news-trio-tag-block-3 > div'
				tag=True
			elif len(tag)==0:
				print(breaking_news_topics[i], 'is a topic')
				topic_grid_selector='#block-views-balanced-news-trio-block-2 > div > div > div'

				# left_news_selector='#block-views-news-trio-topic-block > h2'
				# # left_grid_selector='#block-views-news-trio-topic-block > div'
				# left_grid_selector='#block-views-news-trio-topic-block > div > div.view-content'

				# right_news_selector='#block-views-news-trio-topic-block-2 > h2'
				# # right_grid_selector='#block-views-news-trio-topic-block-2 > div'
				# right_grid_selector='#block-views-news-trio-topic-block-2 > div > div.view-content'

				# center_news_selector='#block-views-news-trio-topic-block-1 > h2'
				# # center_grid_selector='#block-views-news-trio-topic-block-1 > div'
				# center_grid_selector='#block-views-news-trio-topic-block-1 > div > div.view-content'
				# block-views-balanced-news-trio-block-2 > div > div > div

		# getting news from column
		topic_grid=s.select(topic_grid_selector)
		l_news,r_news,c_news=[],[],[]
		
		handle=topic_grid[0]
		l_items=handle.find_all("div",{"class":"news-item left"})
		print(len(l_item))
		r_items=handle.find_all("div",{"class":"news-item right"})
		c_items=handle.find_all("div",{"class":"news-item center"})
		for item in l_items
			l_type=l_item.find("div",{"class":"news-type-label"})
			l_link=l_item.find('a').href
			l_title=l_item.find('a').find('div').text
			print(l_title,l_type,l_link)

			# l_news.append()
			# r_news.append()
			# c_news.append()

		left_news_grid_handle=s.select()
		print(left_news_grid_handle)
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
				topic=breaking_news_topics[i]+'-'+bias.find('img').get('title').split(':',1)[1]
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
			print(breaking_news_topics[i], 'not found')

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
				topic=breaking_news_topics[i]+'-'+bias.find('img').get('title').split(':',1)[1]
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
			print(breaking_news_topics[i], 'not found')

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
				topic=breaking_news_topics[i]+' -'+' moderate'
				center_topics.append(topic)
				center_topics_id.append(i+1)
				center_bias_id.append('3')
				# print(news_bias.find('a').text)
				# print(news_bias.find("div", {"class": "field-content"}))	
	# for title,description,source,bias in zip(left_titles,left_descs,left_src,left_bias):
	# 	print(title.strip(),'\t',source.strip(),'\t',bias.strip(),'\n',description.strip(),'\n')

	# organizing data
	fname="/Users/greysonnewton/Desktop/txt-spch/youtube/youtube_ai/nlp/data/allsides_data/"

	left_df,right_df,center_df=pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
	left_df['topic_id']=left_topics_id
	left_df['bias_id']=left_bias_id
	left_df['topic']=left_topics
	left_df['title']=left_titles
	left_df['source']=left_src
	left_df['bias']=left_bias

	left_df['desc.']=left_descs
	left_df.to_csv(fname+"left_breaking_news.csv", index=False)
	left_df.to_pickle(fname+"left_breaking_news.pkl")

	right_df['topic_id']=right_topics_id
	right_df['bias_id']=right_bias_id
	right_df['topic']=right_topics
	right_df['title']=right_titles
	right_df['source']=right_src
	right_df['bias']=right_bias
	right_df['desc.']=right_descs
	right_df.to_csv(fname+"right_breaking_news.csv", index=False)
	right_df.to_pickle(fname+"right_breaking_news.pkl")

	center_df['topic_id']=center_topics_id
	center_df['bias_id']=center_bias_id
	center_df['topic']=center_topics
	center_df['title']=center_titles
	center_df['source']=center_src
	center_df['bias']=center_bias
	center_df['desc.']=center_descs
	center_df.to_csv(fname+"center_breaking_news.csv", index=False)
	center_df.to_pickle(fname+"center_breaking_news.pkl")

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
	df.to_csv(fname+"breaking_news.csv", index=False)
	df.to_pickle(fname+"breaking_news.pkl")
	# print(df.head())
	# print(left_news)
	page_titles = [title.replace('on Allsides', '') for title in page_titles]
	# print(page_titles)
	# print(page_descriptions)
	# print(left_news)
	# with open('data_names.txt','w+') as f:
	# 	f.write("./allsides_data/breaking_news.pkl")
	# 	f.write("./allsides_data/right_breaking_news.pkl")
	# 	f.write("./allsides_data/left_breaking_news.pkl")
	# 	f.write("./allsides_data/center_breaking_news.pkl")
gather_political_news(url)

song = "done.mp3"
playsound(song)
# columns = ['Conservative Perspective', 'Moderate Perspective', 'Liberal Perspective']


def wait_between(a,b):
		rand=uniform(a, b) 
		sleep(rand)

		
















