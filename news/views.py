from django.shortcuts import render
from django.views.generic import ListView

from .models import Headline

import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup


class IndexView(ListView):
	model = Headline
	template_name = 'news/index.html'


def scrape_national_review():
	session = requests.Session()
	session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
	url = "https://www.nationalreview.com/"
	
	content = session.get(url, verify=False).content

	soup = BeautifulSoup(content, "html.parser")
	articles = soup.select(".home-content-area__primary .post-list-article")

	# links = []
	for article in articles:

		try:
			link = article.find_all('a')[2]['href']
			title = article.find('h4').text.strip()
			if article.find('img'):
				img_source = article.find('img')['data-src']
		except:
			raise Exception(f'Failed to scrape {article}.')

		print(title)
		print(link)
		print(img_source, '\n')


