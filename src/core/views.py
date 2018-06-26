from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Post, Feed
from datetime import datetime
import time

import pandas as pd

import feedparser
from hashlib import md5

def home_view(request):

	# Check if there is a search
	query = request.GET.get('q')
	if query: 
		post_list = Post.objects.all().filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(source_url=query)
		).distinct()
	else:
		post_list = Post.objects.all()

	# Pagination system, 18 per page 
	paginator = Paginator(post_list, 18)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	template = 'home.html'
	context = {'posts': posts}

	return render(request, template, context)


def about_view(request):
	template = 'about.html'

	return render(request, template)

@login_required
def run_view(request):
	
	# Collect guids
	posts = Post.objects.all()
	guids = []
	for post in posts:
		guids.append(post.guid)

	# Get list of feed objects
	feeds = Feed.objects.all()
	for feed_obj in feeds:
		print(feed_obj.title)
		feed_url = feed_obj.url
		feed = feedparser.parse(feed_url)

		articles = feed['items']

		# Go through articles in the feed.
		for article in articles:

			title = article.get('title')
			raw_date = article.get('published')

			# RuntimeWarning: DateTimeField Post.date received a naive datetime (2018-06-26 15:30:52) while time zone support is active.
			date = pd.to_datetime(raw_date)

			source_url = article.get('link')

			content = article.get('description') or article.get(
				'content', [{'value': ''}])[0]['value']
			try:
				new_guid = unicode(md5(article.get("link")).hexdigest())
			except NameError:
				new_guid = md5(article.get("link").encode('utf-8')).hexdigest()
		
			# Save if guid isn't in the database already
			new_posts = []
			if new_guid not in guids:
				print('Post: ', title)
				print('Saving post.\n')
				post = Post(
					feed=feed_obj,
					title=title,
					date=date,
					source_url=source_url,
					content=content,
					guid=new_guid,
				)

				post.save()
				new_posts.append(post)
			else:
				print('\tPost: ', title)
				print('\tPost already in the database.\n')

		context = {
			'new_posts': new_posts,
		}

	return render(request, 'run.html', context)

