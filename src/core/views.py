from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.dateparse import parse_date
from .models import Post, Feed
from datetime import datetime
import time

import pandas as pd

import feedparser
from hashlib import md5

def home_view(request):
	
	post_list = Post.objects.all()
	# query = request.GET.get('q')
	paginator = Paginator(post_list, 18)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	template = 'home.html'
	context = {'posts': posts}

	return render(request, template, context)


def about_view(request):
	template = 'about.html'
	context = {}

	return render(request, template, context)


def run_view(request):

	feeds = Feed.objects.all()
	feed_obj = feeds[0]
	feed_url = feed_obj.url
	

	# feed_url = 'https://www.kdnuggets.com/feed'
	feed = feedparser.parse(feed_url)

	articles = feed['items']
	print(len(articles))

	for article in articles[8:]:
		

		title = article.get('title')
		raw_date = article.get('published')

		date = pd.to_datetime(raw_date)

		source_url = article.get('link')
		content = article.get('description') or article.get(
			"content", [{"value": ""}])[0]["value"]
		try:
			guid = unicode(md5(article.get("link")).hexdigest())
		except NameError:
			guid = md5(article.get("link").encode('utf-8')).hexdigest()
		
		post = Post(
			feed=feed_obj,
			title=title,
			date=date,
			source_url=source_url,
			content=content,
			guid=guid,
		)

		post.save()

	context = {
		'title': title,
		'date': date,
		'source_url': source_url,
	}

	return render(request, 'run.html', context)

