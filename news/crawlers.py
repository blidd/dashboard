from abc import ABC, abstractmethod

from . import wrappers
from .models import Source, Headline

# import requests
# from bs4 import BeautifulSoup

# import os
# import shutil
import logging
logger = logging.getLogger(__name__)


class AbstractBaseCrawler(ABC):
	def __init__(self, slug, client, status='GOOD'):
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
		}
		self.source = Source.objects.get(slug=slug)
		self.client = client
		self.status = status

	@property
	def status(self):
		return self._status
	
	@status.setter
	def status(self, s):
		available_statuses = ['GOOD', 'CRAWLING', 'ERROR']
		if s not in available_statuses:
			return ValueError('Status is not valid.')
		self._status = s

	# @abstractmethod
	# def get_top_stories(self):
	# 	"""Retrieve data of stories on front page or top stories."""

	@abstractmethod
	def update_headlines(self):
		"""Crawls website for top headlines or stories"""

	def crawl(self):
		try:
			self.status = 'CRAWLING'
			self.update_headlines()
			self.status = 'GOOD'
		except:
			self.status = 'ERROR'
			logger.exception('Error occurred while crawling {self.source}.')


class RedditCrawler(AbstractBaseCrawler):
	def __init__(self):
		super().__init__('reddit', wrappers.RedditClient())

	def update_headlines(self):
		stories = self.client.get_top_stories()
		print(stories)


class NationalReviewCrawler(AbstractBaseCrawler):
	def __init__(self):
		super().__init__('national-review', wrappers.NationalReviewClient())

	def update_headlines(self):
		try:
			headlines = self.client.get_top_stories()
			for hl in headlines:
				# Creates the headline if it does not exist, otherwise just updates existing one
				h, _ = Headline.objects.get_or_create(source=self.source, title=hl['title'])
				h.image = hl['img_source']
				h.url = hl['link']
				h.save()
		except: 
			logger.exception('Error occurred while updating headlines for the National Review.')
