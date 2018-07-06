from django.contrib.sitemaps import Sitemap
from core.models import Post, Tag
from django.urls import reverse


class PostsSitemap(Sitemap):
	changefreq = 'monthly'
	priority = 0.5
	protocol = 'https'

	def items(self):
		return Post.objects.filter(is_active=True)

	def lastmod(self, obj):
		return obj.date


class TagsSitemap(Sitemap):
	changefreq = 'monthly'
	priority = 0.5
	protocol = 'https'

	def items(self):
		return Tag.objects.filter(is_active=True)

	def lastmod(self, obj):
		return obj.updated


class StaticSitemap(Sitemap):
	priority = 0.5
	changefreq = 'weekly'
	protocol = 'https'

	def items(self):
		return ['about', 'tags_list']

	def location(self, item):
		return reverse(item)


class HomeSitemap(Sitemap):
	priority = 0.8
	changefreq = 'hourly'
	protocol = 'https'

	def items(self):
		return ['home']

	def location(self, item):
		return reverse(item)