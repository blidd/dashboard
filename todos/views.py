from django.shortcuts import render

from rest_framework import generics

from .models import Todo
from .serializers import TodoSerializer


class TodoList(generics.ListAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer


class TodoDetail(generics.RetrieveAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer