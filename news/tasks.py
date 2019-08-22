 # from __future__ import absolute_import, unicode_literals
from news import wrappers
from news.models import Headline
from celery import shared_task


import logging
logger = logging.getLogger(__name__)
 

@shared_task
def crawl_news_task():
	for client in wrappers.client_registry:
		client_instance = client()
		top_stories = client_instance.get_top_stories()
		
		for s in top_stories:
			h, _ = Headline.objects.get_or_create(
				source=client_instance.source, 
				title=s['title'],
				url=s['link'])