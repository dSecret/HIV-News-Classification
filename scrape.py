import json, re
import requests
from bs4 import BeautifulSoup
import random

					
baselink = "https://timesofindia.indiatimes.com/2010/1/1/archivelist/year-2010,month-1,starttime-"
					
					# fetches links from specific day
def fetchLinks(index):

	print("fething index: ",index)
	r = requests.get(baselink+str(index)+".cms")

	soup = BeautifulSoup(r.text,'html.parser')
	linkDiv = soup.body.div.findAll('table')[1].table
	links = linkDiv.findAll('a')
	links = [link['href'] for link in links]

	# last link is ad
	del(links[len(links)-1])

	print("Links extracted")
	return links

					#retrieve prev saved links and concatenate 
def addLinks(newlinks):
	prevlinks = []
	with open("toi_month_links.json",'r') as links:
		prevlinks = json.load(links)

	with open("toi_month_links.json",'w') as links:
		prevlinks = prevlinks + newlinks
		json.dump(prevlinks,links,indent=4)


					#initialize the params and call associated functions
def fetchAllLinks():
	indexes = range(40179,43476+1)
	for index in indexes:
		links = fetchLinks(index)
		addLinks(links)


					#retrieve all saved links
def getLinks():
	with open("toi_month_links.json",'r') as links:
			allLinks = json.load(links)
	return allLinks	

					#retrieve pages, find articles & title , save 

def fetchPages(allLinks):
	
	reg_hiv = re.compile(r'HIV|HIV+')

	allPages=[]

	for link in  allLinks:
		print("fething...")
		r = requests.get(link)
		print("fetched...")
		
		soup = BeautifulSoup(r.text,'html.parser')
		title = soup.head.title.string
		body = list(soup.findAll("div",{"class":"article_content clearfix"}))

		if len(body)>0:
			article = (" ").join(body[0].stripped_strings)
			matched = reg_hiv.search(article)
			if matched!=None:
				allPages.append({"title":title,"link":link,"body":article})
			else:
				print("Not Found")	
	with open("toi_news_pages.json","w") as news:
		newlinks = json.dump(allPages,news,indent=4)
		print("Saved...")


					#Initiate Link Scrapping

# fetchAllLinks()
				
					#Initiate specific article scrapping

# allLinks = getLinks()
# fetchPages(allLinks)
