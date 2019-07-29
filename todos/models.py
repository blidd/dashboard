from django.db import models

class Todo(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField(null=True, blank=True)
	due = models.DateField(null=True, blank=True)


	def __repr__(self):
		return f'{__class__.__name__}({self.title})'

	def __str__(self):
		return self.title