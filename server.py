from flask import Flask, request,jsonify,url_for,render_template,make_response
import json

app = Flask(__name__)
from google import search,lucky,search3
import urllib,urllib2,urlparse
import re
from query import gen_query
from BeautifulSoup import *
import readline
#try:
#    import bs4 as BeautifulSoup
#except ImportError:
#    import BeautifulSoup

# Request the given URL and return the response page, using the cookie jar.

#text = 'Congress "11" "1812"  "1942" wikipedia'
#query = urllib.quote_plus(text)
#print(lucky("http://www.google.com/search?q="+ query + "&btnI"))


def url_to_title(url):
        if 'wikipedia.org/' in url:
		splits = url.split("/")
                end = splits[-1]
                end = end.replace("_"," ")
                response = re.sub(r'\([^)]*\)', '', end)
               	return response
	else:
		return str(42)

def major(url):
# Open URL, read HTML, and find title
	print(url)
        URLObject = urllib2.urlopen(url)
        html = BeautifulSoup(URLObject.read())
        data = html.find('title')
        title = data.contents[0]
        title = title.replace(' - Wikipedia',"")
        # Print title
        return title.encode('utf-8')


def parse_url(url,query=''):
	if 'search?q=' in url:
		#print("we got a search?")
		results = search(query,stop=1)
                urls = []
                for url in results:
                	urls.append(url)
		try:
			first_result = urls[0]
		except Exception as inst:
			return str(42)
			#first_result = 'NO RESPONSE'
		return url_to_title(first_result)
	elif 'wikipedia' in url:
		splits = url.split("/")
		end = splits[-1]
		end = end.replace("_"," ")
		response = re.sub(r'\([^)]*\)', '', end)
		return response
	else:
		return url

def get_answer(question,silent=1):
	our_q = gen_query(question)
        query = urllib.quote_plus(our_q)
        url = lucky("http://www.google.com/search?q="+ query + "&btnI")
	if silent != 0:
		return(parse_url(url,our_q))

def watson(text):
	answer = get_answer(text)
	#Do filters. 
	answer = answer.replace("History of","")
	answer = answer.replace("Gameplay of","")
	answer = answer.replace("People of","")
	if (answer.lstrip() != str(42)):
		print("BUZZ")
		print('\a')
		answer = "What is " + answer.lstrip() +"?"
		print(answer)
	else:
		print("No buzz")


def test():
	sample = "types of these cards used in digital cameras include MicroSD SDHC & CompactFlash"
	get_answer(sample,0)

#Do this to make it faster
test()
def watson(text):
	answer = get_answer(text)
	#Do filters. 
	answer = answer.replace("History of","")
	answer = answer.replace("Gameplay of","")
	answer = answer.replace("People of","")
	if (answer.lstrip() != str(42)):
		print("BUZZ")
		print('/a')
		answer = "What is " + answer.lstrip() +"?"
		print(answer)
		return(answer)
	else:
		print("No buzz")


@app.route("/api", methods=['GET', 'POST'])
def hello():
    t = str(request.args['code'])
    output = watson(t)
    return jsonify(r=output)


#return str(request.args['callback'] + "({0})".format(output[:-2]))  
    
@app.route("/", methods=['GET', 'POST']) 
def test():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

