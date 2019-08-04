from django.db import models


class Post(models.Model):
	title = models.CharField(max_length=50)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	def __repr__(self):
		return f'{__class__.__name__}({self.title})'
		