# Pull base image
FROM python:3.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /dashboard

# Install dependencies
COPY Pipfile Pipfile.lock /dashboard/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /dashboard/