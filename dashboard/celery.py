from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

app = Celery('dashboard')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
	print(f'Request: {self.request}')


# @app.task
# def crawl_news_task():
# 	clients = [client() for client in wrappers.get_all_clients()]
# 	for c in clients:
# 		_crawl(c)


# def _crawl(client):
# 	top_stories = client.get_top_stories()
# 	for stories in top_stories:
# 		h, _ = Headline.objects.get_or_create(
# 			source=self.source, 
# 			title=hl['title'],
# 			image=hl['img_source'],
# 			url=hl['link'])