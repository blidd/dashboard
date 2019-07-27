from django.shortcuts import render
from django.views.generic import ListView

from .models import Source, Headline
from .crawlers import NationalReviewCrawler, RedditCrawler

import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup
from datetime import timedelta, timezone, datetime

class IndexView(ListView):
	model = Headline
	template_name = 'news/index.html'


def view_reddit(request):

	reddit_crawler = RedditCrawler()
	reddit_crawler.crawl()

	reddit = Source.objects.get(slug='reddit')
	headlines = Headline.objects.filter(source=reddit).order_by('datetime_scraped')[:5]

	context_dict = {
		'source': reddit,
		'headlines': headlines,
	}

	return render(request, 'news/reddit.html', context=context_dict)


def view_nr(request):

	nr_crawler = NationalReviewCrawler()
	nr_crawler.crawl()

	nr = Source.objects.get(slug='national-review')
	headlines = Headline.objects.filter(source=nr).order_by('datetime_scraped')[:5]

	context_dict = {
		'source': nr,
		'headlines': headlines,
	}

	return render(request, 'news/national_review.html', context=context_dict)


# def scrape_national_review(request):
# 	# custom_user = CustomUser.objects.get(user=request.user)
# 	# custom_user.last_scrape = datetime.now(timezone.utc)
# 	# custom_user.save()

# 	session = requests.Session()
# 	session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
# 	url = "https://www.nationalreview.com/"
	
# 	content = session.get(url, verify=False).content

# 	soup = BeautifulSoup(content, "html.parser")
# 	articles = soup.select(".home-content-area__primary .post-list-article")

# 	for article in articles:

# 		title = article.find('h4').text.strip()
# 		link = article.find_all('a')[2]['href']
# 		try:
# 			img_source = article.find('img')['data-src']
# 		except:
# 			print(f'Failed to scrape article image.')
# 			img_source = None

# 		headline = Headline()
# 		headline.title = title
# 		headline.url = link
# 		headline.image = img_source

# 		# print(title)
# 		# print(link)		
# 		# print(img_source)
# 		headline.save()

# 	return render(request, 'news/index.html', context={})


