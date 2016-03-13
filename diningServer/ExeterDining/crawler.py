import urllib.request
from bs4 import BeautifulSoup
import datetime

class Crawler:
	def raw_html(self):
		handle=urllib.request.urlopen("http://www.exeter.edu/student_life/14202_15947.aspx")
		html_gunk = handle.read()
		return html_gunk



if __name__ == '__main__':
	crawl = Crawler()
	print(crawl.raw_html())

