# imports for heise scrap
from bs4 import BeautifulSoup
import requests
import csv
# import for data analysis
import re
from collections import Counter

# this function returns a soup page object
def getPage(url):
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "lxml")
	return soup

# scraper website: heise.de/thema/https
def main():
	file_obj = open("heise_https.csv", "w")
	csvw = csv.writer(file_obj, delimiter = ";")
	
	content = getPage("https://www.heise.de/thema/https")
	
	# determine all pages of topic https
	pages = ["/thema/https"]
	for p in content.find("span", {"class": "pagination"}):
		if (str(p.get("href")) == "None"):
			continue
		else:
			pages.append(p.get("href"))		
		
		
	# write headers into heise_https.csv
	for page in pages:
		content = getPage("https://www.heise.de"+page)
		content = content.findAll("div", {"class": "keywordliste"})
		for c in content:
			cont_nav = c.findAll("nav")
			for head in cont_nav:
				header = head.findAll("header")
				res = ""
				for result in header:
					res+=result.string
					csvw.writerow(result)
	
	file_obj.close()                                # close file
	
	# data analysis: top 3 words in headers
	with open("heise_https.csv") as f:
		doc = f.read()
	# regular expression to find words (included composed words)
	words = re.findall('(?:[^_\W]|-)+', doc)
		
	word_counts = Counter(words)
	test = word_counts.most_common(3)
	
	# prints top 3 words with count
	print("\nThe top 3 words in heise/thema/https-headers are:\n")
	for i in test:
		print(i)

# main program

if __name__ == '__main__':
	main()
