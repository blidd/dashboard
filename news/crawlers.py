from abc import ABC, abstractmethod

from . import clients
from .models import Source, Headline

import logging
logger = logging.getLogger(__name__)


class AbstractBaseCrawler(ABC):
	def __init__(self, slug, client):
		self.source = Source.objects.get(slug=slug)
		self.client = client

	@abstractmethod
	def update_headlines(self):
		"""Crawls website for top headlines or stories"""

	def update_status(self, status):
		self.source.status = status
		self.source.save()

	def crawl(self):
		try:
			self.update_status(Source.CRAWLING)
			self.update_headlines()
			self.update_status(Source.GOOD)
		except:
			slef.update_status(Source.ERROR)
			logger.exception('Error occurred while crawling {self.source}.')


class RedditCrawler(AbstractBaseCrawler):
	def __init__(self):
		super().__init__('reddit', clients.RedditClient())

	def update_headlines(self):
		stories = self.client.get_top_stories()
		print(stories)


class NationalReviewCrawler(AbstractBaseCrawler):
	def __init__(self):
		super().__init__('national-review', clients.NationalReviewClient())

	def update_headlines(self):

		try:
			headlines = self.client.get_front_page()
			for hl in headlines:
				# Creates the headline if it does not exist, otherwise just updates existing one
				h, _ = Headline.objects.get_or_create(source=self.source, title=hl['title'])
				h.image = hl['img_source']
				h.url = hl['link']
				h.save()
		except:
			logger.exception('Error occurred while updating headlines for the National Review.')
