from django.utils import timezone

from .models import Headline

import os
import logging
import shutil
from abc import ABC

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AbstractBaseClient(ABC):
	def __init__(self):
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
		}


class RedditClient(AbstractBaseClient):

	def get_top_stories(self):
		stories = []

		try:
			r = requests.get('https://www.reddit.com/.json', headers=self.headers)
			results = r.json()
			stories = results['data']['children']
		except ValueError:
			print("Error occurred while querying Reddit API")

		return stories


class NationalReviewClient(AbstractBaseClient):

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







