from flask import Flask
from flask import request
from bs4 import BeautifulSoup

from googlesearch import search
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import requests

app=Flask(__name__)
@app.route("/")
def home():
    return "hello world"
songlyrics=""
@app.route("/lyrics",methods=['GET','POST'])
def lyrics():
	url=request.args.get('lyricsUrl')
	# songlyrics=""
	global songlyrics
	recursive(url) #this function invokes requests.get method
 ##############################
 #This piece of code is for using selenium method instead of requests.get
	# driver.get(url)
	# html=BeautifulSoup(driver.page_source,'html.parser')
	# songlyricsTemp=html.find('div',class_='lyrics').get_text(separator="\n")
	# print(songlyricsTemp)
	# songlyrics=songlyricsTemp
 ##############################
	return songlyrics

#As the requests.get method is a hit and miss for retriving lyrics but is still faster
#than selenium (sometimes, sometimes really slow as well) to get the lyrics, the recursive function is called again and again until the
#lyrics are finally obtained (takes 3-4 times max) and the value is set in the songlyrics global variable
#from where it is returned to the view.
def recursive(url):
	global songlyrics
	print("recursive")
	try:
		page=requests.get(url)
		html=BeautifulSoup(page.text,'html.parser')
		songlyricsTemp=html.find('div',class_='lyrics').get_text()
		print(songlyricsTemp)
		songlyrics=songlyricsTemp
	except (TypeError,AttributeError) as e:
		recursive(url)

#The Method to obtain lyrics from azlyrics.com is much much faster and accurate than the genius.com method
@app.route("/lyricsaz",methods=['GET','POST'])
def lyricsaz():
	url=request.args.get('lyricsUrl')
	page=requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")
	lyrics_tags = soup.find_all("div", attrs={"class": None, "id": None})
	print("the length is ",len(lyrics_tags))
	lyrics = [tag.getText() for tag in lyrics_tags]

	print(lyrics)
	return lyrics[0]

@app.route("/details",methods=['GET','POST'])
def getSongInformation():
	track=request.args.get('track')
	artist=request.args.get('artist')
	print(track,artist)
	query="azlyrics "+track+" "+artist+" lyrics"
	queries=[]
	domainRegex="azlyrics.com/lyrics"
	for j in search(query, tld="com", num=5, stop=5, pause=2):
		if domainRegex in j:
			queries.append(j)
   
	lyrics=""
	if len(queries)!=0:
		lyrics=findLyrics(queries[0]) #queries[0] is the azlyrics url
		return lyrics
	else:
		return "Lyrics Could Not Be Found"
	# allqueries=""
	# for i in queries:
	# 	allqueries+=i+"<br>"
	# return allqueries

def findLyrics(url):
	page=requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")
	lyrics_tags = soup.find_all("div", attrs={"class": None, "id": None})
	lyrics = [tag.getText() for tag in lyrics_tags]
	print(lyrics)
	return lyrics[0].replace("\n","<br>")
    

if __name__=="__main__":
	# chrome_options = Options()
	# chrome_options.add_argument("--headless")
	# chrome_options.add_argument('--no-proxy-server')
	# chrome_options.add_argument("--proxy-server='direct://'");
	# chrome_options.add_argument("--proxy-bypass-list=*");
	# driver=webdriver.Chrome(chrome_options=chrome_options)
	app.run(host='0.0.0.0',port=5001,debug=True)
# 	getLyrics("https://genius.com/The-strokes-eternal-summer-lyrics")
