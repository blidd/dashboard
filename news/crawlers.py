from abc import ABC, abstractmethod

from . import clients
from .models import Source, Headline

import logging
logger = logging.getLogger(__name__)


class AbstractBaseCrawler(ABC):
	def __init__(self, slug, status='GOOD'):
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
		}
		self.source = Source.objects.get(slug=slug)
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

	@abstractmethod
	def update_headlines(self):
		"""Crawls website for top headlines or stories"""

	def crawl(self):
		try:
			self.client.status = 'CRAWLING'
			self.update_headlines()
			self.client.status = 'GOOD'
		except:
			self.client.status = 'ERROR'
			logger.exception('Error occurred while crawling {self.source}.')


class RedditCrawler(AbstractBaseCrawler):
	def __init__(self):
		super().__init__('reddit')

	def get_top_stories(self):
		stories = []
		try:
			r = requests.get('https://www.reddit.com/.json', headers=self.headers)
			results = r.json()
			stories = results['data']['children']
		except ValueError:
			logger.exception("Error occurred while querying Reddit API")
		return stories

	def update_headlines(self):
		stories = self.get_top_stories()
		print(stories)


class NationalReviewCrawler(AbstractBaseCrawler):
	def __init__(self):
		super().__init__('national-review')

	def update_headlines(self):
		try:
			headlines = self.get_front_page()
			for hl in headlines:
				# Creates the headline if it does not exist, otherwise just updates existing one
				h, _ = Headline.objects.get_or_create(source=self.source, title=hl['title'])
				h.image = hl['img_source']
				h.url = hl['link']
				h.save()
		except: 
			logger.exception('Error occurred while updating headlines for the National Review.')

	def get_front_page(self):
		results = []

		r = requests.get('https://www.nationalreview.com/', headers=self.headers)
		soup = BeautifulSoup(r.content, "html.parser")
		articles = soup.select('.home-content-area__primary .post-list-article')

		for article in articles:
			title = article.find('h4').text.strip()
			link = article.find_all('a')[2]['href']

			try:
				img_source = article.find('img')['data-src']

				# media_root = '/Users/brianli/workspace/django/dashboard/media'
				# if not img_source.starts_with(('data:image', 'javascript')):
				# 	local_filename = image_source.split('/')[-1].split('?')[0]
				# 	r = requests.get(img_source, stream=True, verify=False)
				# 	with open(local_filename, 'wb') as f:
				# 		for chunk in r.iter_content(chunk_size=1024):
				# 			f.write(chunk)
				# 	image_abs_path = os.path.abspath(local_filename)
				# 	shutil.move(image_abs_path, media_root)
				# else:
				# 	raise Exception('Image not the correct format.')
			except:
				print(f'Failed to scrape article image.')
				# local_filename = None
				img_source = None

			data = {
				'title': title,
				'link': link,
				'img_source': img_source,
			}

			results.append(data)
		return results
