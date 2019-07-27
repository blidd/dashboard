from abc import ABC, abstractmethod

from . import clients
from .models import Source, Headline


class AbstractBaseCrawler(ABC):
	def __init__(self, slug, client):
		self.source = Source.objects.get(slug=slug)
		self.client = client

	@abstractmethod
	def update_headlines(self):
		"""Crawls front page to check if headlines have changed"""

	def crawl(self):
		try:
			self.update_headlines()
			self.source.save()
		except:
			print("Failed to crawl website.")


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
		headlines = self.client.get_front_page()
		print(headlines)