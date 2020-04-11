from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('test', views.view_crawl),
    path('national-review', views.view_nr, name='national-review'),
    path('reddit', views.view_reddit, name='reddit'),
]
