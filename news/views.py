from django.shortcuts import render
from django.views.generic import ListView

from .models import Source, Headline

# import requests

# from bs4 import BeautifulSoup
# from datetime import timedelta, timezone, datetime


class IndexView(ListView):
    model = Headline
    template_name = 'news/index.html'


def view_reddit(request):

    reddit = Source.objects.get(slug='reddit')
    headlines = Headline.objects.filter(
        source=reddit).order_by('-datetime_scraped')[:10]

    context_dict = {
        'source': reddit,
        'headlines': headlines,
    }

    return render(request, 'news/reddit.html', context=context_dict)


def view_nr(request):

    nr = Source.objects.get(slug='national-review')
    headlines = Headline.objects.filter(
        source=nr).order_by('-datetime_scraped')[:10]

    context_dict = {
        'source': nr,
        'headlines': headlines,
    }

    return render(request, 'news/national_review.html', context=context_dict)
