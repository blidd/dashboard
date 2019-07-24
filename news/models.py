from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Headline(models.Model):
	title = models.CharField(max_length=120)
	image = models.ImageField()
	url = models.TextField()

	def __str__(self):
		return self.title


class CustomUser(AbstractUser):
	last_scrape = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.user}-{self.last_scrape}"