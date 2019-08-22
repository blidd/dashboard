from django.utils import timezone
from news.models import Source, Headline
import secret

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

	def __init__(self, source, base_url, url_path, url_params):
		self.source = source
		self.url = build_url(base_url, url_path, url_params)
		self.headers = {"User-Agent": "DashboardNewsClient/0.0.1 by BLi/Technolojeezus"}


	@staticmethod
	def build_url(base_url, url_path, url_params):
		return self.base_url + self.url_path + '?' + '&'.join([f'{param}={value}' for param, value in url_params.items()])


	@abstractmethod
	def get_top_stories(self):
		"""Collects top stories from the target website"""


@register_client(active=False)
class RedditClient(AbstractBaseClient):

	def __init__(self, url_path, url_params=None):
		super().__init__(
			Source.objects.get(slug='reddit'),
			'https://oauth.reddit.com/api/v1',
			url_path,
			url_params,
		)

		# Request and add Reddit access token to request header for Application-Only OAuth
		r = requests.post(
			'https://www.reddit.com/api/v1/access_token',
			data={'grant_type': 'client_credentials'},
			headers=self.headers,
			auth=(secret.reddit_client_id, secret.reddit_client_secret)
		)
		try:
			token = r.json()['access_token']
			self.headers['Authorization'] = 'bearer ' + token
		except ValueError:
			logger.exception("Error occurred while requesting Reddit access token.")
		

	@classmethod
	def subreddit_learnjavascript(cls):
		return cls('/r/learnjavascript/hot', {'limit': 5})


	# Query the most popular posts off Reddit
	def get_top_stories(self):

		# try:
		response = requests.get(self.url, headers=self.headers)
		try:
			results = response.json()['data']['children']
			stories = [{'title': r['data']['title'], 'link': 'https://www.reddit.com' + r['data']['permalink']} for r in results]
			return stories
		except ValueError:
			logger.exception(f'Error occurred while querying Reddit API at {self.url}')
			return None


@register_client()
class NYTimesClient(AbstractBaseClient):

	def __init__(self, url_path, url_params={'api-key': secret.nytimes_api_key}):
		return super().__init__(
			Source.objects.get(slug='new-york-times'),
			'https://api.nytimes.com/svc/topstories/v2/home.json',
			url_path,
			url_params,
		)

	def get_top_stories(self):
		sections = ('Climate', 'Business', 'Politics', 'World')

		response = requests.get(self.url, headers=self.headers)
		results = response.json()['results']
		stories = [{'title': r['title'], 'url': r['url']} for r in results if r['section'] in sections]
		return stories


@register_client()
class NationalReviewClient(AbstractBaseClient):

	def __init__(self, url_params=None):
		return super().__init__(
			Source.objects.get(slug='national-review'), 
			'https://nationalreview.com',
			url_params
		)

	def get_top_stories(self):
		stories = []

		r = requests.get(self.url, headers=self.headers)
		soup = BeautifulSoup(r.content, "html.parser")
		articles = soup.select('.home-content-area__primary .post-list-article')

		for article in articles:
			title = article.find('h4').text.strip()
			link = article.find_all('a')[2]['href']
			data = {
				'title': title,
				'link': link,
			}
			stories.append(data)
			
		return stories


