from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify

import datetime

# Create your models here.

class Source(models.Model):

	GOOD = 'G'
	ERROR = 'E'
	CRAWLING = 'C'
	CURRENT_STATUS = (
		(GOOD, 'good'), 
		(ERROR, 'error'), 
		(CRAWLING, 'running')
		)


	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=30, unique=True)
	url = models.URLField()
	story_url = models.URLField(null=True)
	last_crawled = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=1, default=GOOD, choices=CURRENT_STATUS)

	class Meta:
		verbose_name = 'Media source'
		verbose_name_plural = 'Media sources'
		ordering = ('name',)

	def __repr__(self):
		return f'{__class__.__name__}({self.name!r}, {self.status!r})'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)


class Headline(models.Model):
	source = models.ForeignKey(Source, related_name='headlines', on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=120)
	image = models.ImageField(null=True)
	url = models.URLField(null=True)
	datetime_scraped = models.DateTimeField(auto_now_add=True)
	datetime_updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Headline'
		verbose_name_plural = 'Headlines'
		ordering = ('title',)

	def __repr__(self):
		return f'{__class__.__name__}({self.title!r}, {self.source!r})'

	def __str__(self):
		return self.title


# class CustomUser(AbstractUser):
# 	last_scrape = models.DateTimeField(null=True, blank=True)

# 	def __str__(self):
# 		return f"{self.user}-{self.last_scrape}"

