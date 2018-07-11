from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.dateparse import parse_date
from django.utils.text import slugify

from core.models import Post, Feed, Tag, OtherTag

from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
from hashlib import md5
import pandas as pd
import logging

# Logger sestup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(message)s')
# formatter = logging.Formatter('%(created)f:%(message)s')
# print(os.getcwd())
print('DEBUG: ', settings.DEBUG)
if settings.DEBUG:
	file_handler = logging.FileHandler('../log/parser.log')
else: 
	file_handler = logging.FileHandler('/var/www/datasciencevault/log/parser.log')

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


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

# Parser
def run():
	new_posts_counter = 0
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
	feeds = Feed.objects.filter(is_active=True)
	new_posts = []
	for feed_obj in feeds:
		# logger.debug(feed_obj.title)
		# logger.info('-')
		url_feed = feed_obj.url_feed
		feed = feedparser.parse(url_feed)

		articles = feed['items']

		# Go through articles in the feed.
		for article in articles:

			is_active = True
			
			title = article.get('title')
			if not title: 
				is_active = False
			raw_date = article.get('published')
			# Check if data isn't in corrupted format
			try:
				date = pd.to_datetime(raw_date, utc=True)
				if not date:
					date = pd.Timestamp.utcnow()
					is_active = False

			except:
				date = pd.Timestamp.utcnow()
				logger.exception('Corrupted Date.', exc_info=True)
				is_active = False
			
			source_url = article.get('link')

			content = article.get('description') or article.get(
				'content', [{'value': ''}])[0]['value']
			content = normalize_content(content)

			slug = slugify(title)

			try:
				new_guid = unicode(md5(article.get("link")).hexdigest())
			except NameError:
				new_guid = md5(article.get("link").encode('utf-8')).hexdigest()
	
			# Save if guid isn't in the database already
			if new_guid not in guids:
				logger.info('Feed: {:<20}\nPost: {}'.format(feed_obj.title.upper(), title))
				
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
				# Checks if variables are not empty		
				if all([feed_obj, title, date, source_url, new_guid, slug]):
					post = Post(
						feed=feed_obj,
						title=title,
						date=date,
						source_url=source_url,
						content=content,
						guid=new_guid,
						slug=slug,
						is_active=is_active,
					)
					post.save()
					post.tags.add(*tags_to_add)
					post.other_tags.add(*other_tags_to_add)
					post.save()
					new_posts.append(post)
					new_posts_counter += 1
					logger.info('Saving post.\n')
				else:
					logger.debug('Something is missing!')
			else:
				logger.debug('--Feed: {:<20}\nPost: {}'.format(feed_obj.title.upper(), title))
				logger.debug('--Post already in the database.')
				logger.debug('--SKIPPING THE REST.\n')
				break


	logger.info('\n-\n{} POSTS ADDED.\n-\n'.format(new_posts_counter))
	
	return 
