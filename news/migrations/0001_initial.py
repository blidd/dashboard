# Generated by Django 3.0.5 on 2020-04-11 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('url', models.URLField()),
                ('story_url', models.URLField(null=True)),
                ('last_crawled', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('G', 'good'), ('E', 'error'), ('C', 'running')], default='G', max_length=1)),
            ],
            options={
                'verbose_name': 'Media source',
                'verbose_name_plural': 'Media sources',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Headline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('url', models.URLField(null=True)),
                ('datetime_scraped', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headlines', to='news.Source')),
            ],
            options={
                'verbose_name': 'Headline',
                'verbose_name_plural': 'Headlines',
                'ordering': ('title',),
            },
        ),
    ]
