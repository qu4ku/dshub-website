"""

"""

import os
import django
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.dateparse import parse_date
from django.utils.text import slugify

import sys
sys.path.append('../project/settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local')
django.setup()


# from .models import Post, Feed, Tag, OtherTag
from core.models import Post, Feed, Tag, OtherTag

from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
from hashlib import md5
import pandas as pd


def normalize_tag(tag):
	""" Converts "- sometag -" to "tag"""
	tag = tag.strip('-')

	# Fix for HTML entities
	tag = BeautifulSoup(tag, 'html.parser').prettify()
	tag = tag.strip().lower()
	tag = slugify(tag)
	tag = tag.replace(' ', '-')

	return tag

def normalize_content(content):
	""" Cleaning form html tags """
	content = BeautifulSoup(content, 'html.parser').get_text()
	return content

# @login_required
def run():
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

	# Get list of feed objects
	feeds = Feed.objects.all()
	new_posts = []
	for feed_obj in feeds:
		print(feed_obj.title)
		print()
		url_feed = feed_obj.url_feed
		feed = feedparser.parse(url_feed)

		articles = feed['items']

		# Go through articles in the feed.
		for article in articles:

			title = article.get('title')
			raw_date = article.get('published')

			# RuntimeWarning: DateTimeField Post.date received a naive datetime (2018-06-26 15:30:52) while time zone support is active.
			date = pd.to_datetime(raw_date, utc=True)

			source_url = article.get('link')

			content = article.get('description') or article.get(
				'content', [{'value': ''}])[0]['value']
			content = normalize_content(content)

			slug = slugify(title)

			try:
				new_guid = unicode(md5(article.get("link")).hexdigest())
			except NameError:
				new_guid = md5(article.get("link").encode('utf-8')).hexdigest()
	
			# Create new OtherTag if tag doesn't exist
			tags_to_add = []
			other_tags_to_add = []
			for tag_dict in article.get('tags', []):
				tag_name = tag_dict.get('term') or tag_dict.get('label')
				tag_name = normalize_tag(tag_name)
				
				try:
					is_in_tags = Tag.objects.get(slug=tag_name)
				except:
					is_in_tags = None
				try:
					is_in_other_tags = OtherTag.objects.get(slug=tag_name)
				except:
					is_in_other_tags = None

				if is_in_tags:
					tags_to_add.append(is_in_tags)
				elif is_in_other_tags:
					other_tags_to_add.append(is_in_other_tags)
				# Create new Other tag
				else: 
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
					slug=slug,
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

	return

if __name__ == '__main__':
	run_view()