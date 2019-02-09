from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.dateparse import parse_date
from django.utils.text import slugify

from .models import Post, Feed, Tag, OtherTag


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
		).distinct().filter(is_active=True, is_hidden=False)
	else:
		post_list = Post.objects.filter(is_active=True, is_hidden=False)

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

	tags = post.tags.all() # Get categories objects
	print(tags)
	
	tags_dict = {}
	post_cap = 3
	for tag in tags:

		top_posts =  Post.objects.all().filter(tags=tag)[:post_cap]
		tags_dict[tag] = top_posts
	print(tags_dict)
	context = {
		'post': post,
		'tags': tags_dict,
		}

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

	query = request.GET.get('q')

	if query: 
		post_list = Post.objects.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(source_url=query)
		).distinct().filter(is_active=True, is_hidden=False)
	else:
		post_list = Post.objects.filter(is_active=True, is_hidden=False)

	paginator = Paginator(post_list, 18)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	template = 'search-results.html'
	context = {
		'posts': posts,
		'query': query,
	}
	
	return render(request, template, context)
