from django.utils import timezone
from news.models import Source, Headline

import os

import shutil
import inspect
import sys
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)


client_registry = set()

def register_client(active=True):
	def decorate(client_cls):
		if active:
			client_registry.add(client_cls)
		else:
			client_registry.discard(client_cls)

		return client_cls
	return decorate


class AbstractBaseClient(ABC):

	def __init__(self, source):
		self.source = source
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
		}

	@abstractmethod
	def get_top_stories(self):
		"""Collects top stories from the target website"""


@register_client(active=False)
class RedditClient(AbstractBaseClient):

	def __init__(self):
		return super().__init__(Source.objects.get(slug='reddit'))

	def get_top_stories(self):
		stories = []

		try:
			r = requests.get('https://www.reddit.com/.json', headers=self.headers)
			results = r.json()
			stories = results['data']['children']
		except ValueError:
			logger.exception("Error occurred while querying Reddit API")

		return stories


@register_client()
class NationalReviewClient(AbstractBaseClient):

	def __init__(self):
		return super().__init__(Source.objects.get(slug='national-review'))

	def get_top_stories(self):
		stories = []

		r = requests.get('https://www.nationalreview.com/', headers=self.headers)
		soup = BeautifulSoup(r.content, "html.parser")
		articles = soup.select('.home-content-area__primary .post-list-article')

		for article in articles:
			title = article.find('h4').text.strip()
			link = article.find_all('a')[2]['href']

			# try:
			# 	img_source = article.find('img')['data-src']
			# except:
			# 	print(f'Failed to scrape article image.')
			# 	# local_filename = None
			# 	img_source = None

			data = {
				'title': title,
				'link': link,
				# 'img_source': img_source,
			}
			stories.append(data)
			
		return stories

