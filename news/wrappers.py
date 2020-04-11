from news.models import Source
from django.template.defaultfilters import slugify
import secret

from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)


# String const variables

REDDIT_NAME = 'Reddit'
REDDIT_BASE_URL = 'https://oauth.reddit.com/api/v1'

NYTIMES_NAME = 'New York Times'
NYTIMES_BASE_URL = 'https://api.nytimes.com'

NATIONAL_REVIEW_NAME = 'National Review'
NATIONAL_REVIEW_BASE_URL = 'https://www.nationalreview.com'


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

    def __init__(self):
        self.headers = {
            "User-Agent": "DashboardNewsClient/0.0.1 by BLi/Technolojeezus"
        }

    @staticmethod
    def build_url(base_url, url_path, url_params=None):
        return base_url + url_path + '?' + '&'.\
            join([f'{param}={value}'
                  for param, value in url_params.items()]) \
            if url_params else base_url + url_path

    @abstractmethod
    def get_top_stories(self):
        """Collects top stories from the target website"""


@register_client(active=False)
class RedditClient(AbstractBaseClient):

    def __init__(self):
        super().__init__()

        self.source, _ = Source.objects.get_or_create(
            name=REDDIT_NAME,
            slug=slugify(REDDIT_NAME),
            url=REDDIT_BASE_URL)

        # Request and add Reddit access token to request header for
        # Application-Only OAuth
        r = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            data={'grant_type': 'client_credentials'},
            headers=self.headers,
            auth=(secret.reddit_client_id, secret.reddit_client_secret)
        )
        try:
            token = r.json()['access_token']
            self.headers['Authorization'] = 'bearer ' + token
        except ValueError as e:
            logger.exception(
                e,
                "Error occurred while requesting Reddit access token.")

    # **WARNING**: totally untested
    def get_subreddit_learnjavascript(self):

        url = self.build_url(
            self.source.url,
            '/r/learnjavascript/hot',
            {'limit': 5}
        )

        response = requests.get(url, headers=self.headers)
        try:
            results = response.json()['data']['children']
            stories = [{'title': r['data']['title'], 'link': 'https://www.reddit.com' +
                        r['data']['permalink']} for r in results]
            return stories
        except ValueError:
            logger.exception(
                f'Error occurred while querying Reddit API at {url}')
            return None

    # Query the most popular posts off Reddit
    def get_top_stories(self):
        url = self.build_url(self.source.url, '/subreddits/popular')

        response = requests.get(url, headers=self.headers)
        try:
            results = response.json()['data']['children']
            stories = [{'title': r['data']['title'], 'link': 'https://www.reddit.com' +
                        r['data']['permalink']} for r in results]
            return stories
        except ValueError:
            logger.exception(
                f'Error occurred while querying Reddit API at {url}')
            return None


@register_client()
class NYTimesClient(AbstractBaseClient):

    def __init__(self):
        super().__init__()

        self.source, _ = Source.objects.get_or_create(
            name=NYTIMES_NAME,
            slug=slugify(NYTIMES_NAME),
            url=NYTIMES_BASE_URL)

    def get_top_stories(self):
        url = self.build_url(
            self.source.url,
            '/svc/topstories/v2/home.json',
            {'api-key': secret.nytimes_api_key}
        )

        sections = ('Climate', 'Business', 'Politics', 'World')

        response = requests.get(url, headers=self.headers)
        results = response.json()['results']
        stories = [{'title': r['title'], 'url': r['url']}
                   for r in results if r['section'] in sections]
        return stories


@register_client()
class NationalReviewClient(AbstractBaseClient):

    def __init__(self, url_params=None):
        super().__init__()

        self.source, _ = Source.objects.get_or_create(
            name=NATIONAL_REVIEW_NAME,
            slug=slugify(NATIONAL_REVIEW_NAME),
            url=NATIONAL_REVIEW_BASE_URL)

    def get_top_stories(self):

        url = self.build_url(
            self.source.url,
            ''
        )

        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        articles = soup.select(
            '.home-content-area__primary .post-list-article')

        stories = []
        for article in articles:
            title = article.find('h4').text.strip()
            link = article.find_all('a')[2]['href']
            data = {
                'title': title,
                'link': link,
            }
            stories.append(data)

        return stories
