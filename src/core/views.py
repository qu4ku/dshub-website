from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Post, Feed, Tag, OtherTag
from datetime import datetime
import time

from bs4 import BeautifulSoup

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



def normalize_tag(tag):
	""" Converts "- sometag -" to "tag"""
	tag = tag.strip('-')

	# Fix for HTML entities
	tag = BeautifulSoup(tag, 'html.parser').prettify()
	tag = tag.strip().lower()
	tag = tag.replace(' ', '-')
	return tag

def normalize_content(content):
	""" Cleaning form html tags """
	content = BeautifulSoup(content, 'html.parser').get_text()
	return content

@login_required
def run_view(request):
	
	# Collect guids, tags, and new_tags
	posts = Post.objects.all()
	guids = []
	for post in posts:
		guids.append(post.guid)

	tag_objs = Tag.objects.all()
	tags = []
	for tag_obj in tag_objs:
		tags.append(tag_obj.slug)

	other_tag_objs = OtherTag.objects.all()
	other_tags = []
	for other_tag_obj in other_tag_objs:
		other_tags.append(other_tag_obj.slug)
	print(tags)
	print(other_tags)

	# Get list of feed objects
	feeds = Feed.objects.all()
	new_posts = []
	for feed_obj in feeds:
		print(feed_obj.title)
		print()
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
			content = normalize_content(content)

			try:
				new_guid = unicode(md5(article.get("link")).hexdigest())
			except NameError:
				new_guid = md5(article.get("link").encode('utf-8')).hexdigest()
			
			# Creates new OtherTag if tag doesn't exist
			tags_to_add = []
			other_tags_to_add = []
			for tag_dict in article.get('tags', []):
				tag_name = tag_dict.get('term') or tag_dict.get('label')
				tag_name = normalize_tag(tag_name)
				print(tag_name)
				try:
					is_in_tags = Tag.objects.get(slug=tag_name)
				except:
					is_in_tags = None
				try:
					is_in_other_tags = OtherTag.objects.get(slug=tag_name)
				except:
					is_in_other_tags = None
				if is_in_tags:
					print(tag_name, 'in tags.')
					tags_to_add.append(is_in_tags)
				elif is_in_other_tags:
					other_tags_to_add.append(is_in_other_tags)
				else: # Create new Other tag
					print(tag_name, 'in otehr tags.')
					new_other_tag = OtherTag(
						slug=tag_name,
					)
					new_other_tag.save()

			# Save if guid isn't in the database already
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
				post.tags.add(*tags_to_add)
				post.other_tags.add(*other_tags_to_add)
				post.save()
				new_posts.append(post)
			else:
				print('\tPost: ', title)
				print('\tPost already in the database.\n')

				print('SKIPPING THE REST.\n')
				break

		context = {
			'new_posts': new_posts,
		}

	return render(request, 'run.html', context)

