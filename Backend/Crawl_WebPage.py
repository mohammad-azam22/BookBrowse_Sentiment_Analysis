from urllib.error import HTTPError
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys

def crawlPage():

	urlFile = open("url.txt", "r")
	reviewURL = urlFile.readline()

	page_no = 1
	title = reviewURL.split("/")[-1]
	file = open("reviews.txt", "w")
	
	flag = True
	while(flag):

		words = reviewURL.split("/")
		words[3] = "reader_reviews"
		words[-1] = "page"


		words.append(str(page_no))
		words.append("order/dt")
		words.append(title)
		words.append("#reader_reviews")

		newURL = "/".join(words)

		req = Request(url=newURL)    # making Request class object
		req.add_header('user-agent',  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
		try:
			rawpage = urlopen(req).read()    # sending request to the server and getting raw html page
			soup = BeautifulSoup(rawpage, 'html5lib')    # parsing html page
			content = soup.find("div", {"id":"readerreviews"})    # getting div tag with id readerreviews

			blocks = content.findAll("div", {"class":"showmore"})
			if (len(blocks) == 0):
				break
			else:
				for block in blocks:
					file.write(block.text + "\n")
					# print(block.text)
					# print()
		except HTTPError as http_err:
				print(http_err)	
				break
		finally:
			page_no = page_no + 1
	
	file.close()


if __name__ == "__main__":
	crawlPage()