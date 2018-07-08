from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.dateparse import parse_date
from django.utils.text import slugify

from .models import Post, Feed, Tag, OtherTag

from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
from hashlib import md5
import pandas as pd


def generate_top_tags(cap=20):
	"""Generates sorted list of tag/number_of_occurances pairs.
	
	Args:
		cap (int): max nubmer of tags to return.
	Returns: 
		list: List of (tag, number_of_occurances) tuples.
	"""

	tags = Tag.objects.filter(is_active=True)

	tag_num = []
	for tag in tags:
		tag_num.append((tag.slug, tag.post_set.count()))
	# Tags that occured once or more only
	tag_num = [tag for tag in tag_num if tag[1] > 0]
	tag_num_sorted = sorted(tag_num, key=lambda x: x[1], reverse=True)

	return tag_num_sorted[:cap]


def home_view(request):
	# Check if there is a search query
	query = request.GET.get('q')
	if query: 
		post_list = Post.objects.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(source_url=query)
		).distinct().filter(is_active=True)
	else:
		post_list = Post.objects.filter(is_active=True)

	# Pagination system, 18 posts per page 
	paginator = Paginator(post_list, 18)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	top_tags = generate_top_tags()

	template = 'home.html'
	context = {
		'posts': posts,
		'tags': top_tags,
	}

	return render(request, template, context)


def post_detail_view(request, slug):
	template = 'post-detail.html'
	# Get a list in case there are more than one occurances
	post = get_list_or_404(Post, slug=slug, is_active=True)
	post = post[0]

	context = {'post': post}

	return render(request, template, context)


def about_view(request):
	template = 'about.html'

	return render(request, template)


def tags_list_view(request):

	tags = generate_top_tags(100)

	template = 'tags.html'
	context = {'tags': tags,}
	return render(request, template, context)


def other_tags_list_view(request):
	# Generate tag, number of post by tag pair and then sort it.
	tags = OtherTag.objects.all()

	tag_num = []
	for tag in tags:
		tag_num.append((tag.slug, tag.post_set.count()))
	# tag_num = [tag for tag in tag_num if tag[1] > 0]
	tag_num_sorted = sorted(tag_num, key=lambda x: x[1], reverse=True)
	template = 'other-tags.html'
	context = {'tags': tag_num_sorted,}
	return render(request, template, context)


def tag_view(request, slug):
	tag = get_object_or_404(Tag, slug=slug, is_active=True)
	post_list = Post.objects.filter(tags=tag)
	paginator = Paginator(post_list, 18)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	template = 'tag.html'
	context = {
		'posts': posts,
		'tag': tag,
	}

	return render(request, template, context)


def search_view(request):
	post_list = Post.objects.filter(is_active=True)
	query = request.GET.get('q')

	if query: 
		post_list = Post.objects.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(source_url=query)
		).distinct().filter(is_active=True)
	else:
		post_list = Post.objects.filter(is_active=True)

	paginator = Paginator(post_list, 18)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	template = 'search-results.html'
	context = {
		'posts': posts,
		'query': query,
	}
	return render(request, template, context)


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


@login_required
def run_view(request):
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
		print(feed_obj.title)
		print()
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
			except:
				print('Corrupted Date.')
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
				print('Post: ', title)
				print('Saving post.\n')
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
			else:
				print('\tPost: ', title)
				print('\tPost already in the database.\n')
				print('SKIPPING THE REST.\n')
				break

		context = {
			'new_posts': new_posts,
		}

	print('\n-----\n{} POSTS AADDED.\n------\n'.format(new_posts_counter))
	
	return render(request, 'run.html', context)
