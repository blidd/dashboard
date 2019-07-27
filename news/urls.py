from django.urls import path
from . import views

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('national-review', views.view_nr, name='national-review'),
	path('reddit', views.view_reddit, name='reddit'),
]