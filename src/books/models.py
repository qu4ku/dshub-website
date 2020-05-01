from django.db import models
from django.urls import reverse


class BookCategory(models.Model):
	"""
	BookCategory model. 

	Works as a category of a book but aslo as more general model for category subpage.
	"""

	class Meta:
		verbose_name = 'Book Category'
		verbose_name_plural = 'Book Categories'
		db_table = 'category'
		ordering = ('title',)

	# Do not turn it off once is on: seo
	is_active = models.BooleanField(
		help_text='If available the category page will be published online.',
		default=False
	)
	title = models.CharField(
		help_text='Title, used in meta tags by default',
		max_length=200
	)
	slug = models.SlugField(
		help_text='Slug for the category subpage.',
		unique=True
	)

	# Used to generate subpage
	headline = models.CharField(
		help_text='Headline/H1 text for the category subpage.',
		max_length=200, 
		null=True, 
		blank=True
	)
	description = models.TextField(
		help_text='Description/H2 text for the category subpage.',
		null=True, 
		blank=True
	)

	# Seo
	seo_title = models.CharField(
		help_text='Used in meta title tag if available.',
		max_length=60, 
		null=True,
		blank=True
	)
	seo_description = models.CharField(
		help_text='Used in meta description tag if available.',
		max_length=165, 
		null=True, 
		blank=True
	)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book_category', kwargs={'slug': self.slug})
	

class Book(models.Model):
	""" Book model. """

	class Meta:
		verbose_name = 'Book'
		verbose_name_plural = 'Books'
		db_table = 'book'
		ordering = ('title',)

	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200, null=True, blank=True)
	publication_date = models.DateField(null=True, blank=True)
	rating_goodreads = models.CharField(max_length=20, null=True, blank=True, default='NA')
	rating_amazon = models.CharField(max_length=20, null=True, blank=True, default='NA')
	url_goodreads = models.URLField(
		max_length=250,
		help_text='Url to goodreads.',
		null=True,
		blank=True
	)
	url = models.URLField(
		max_length=250,
		help_text='Url to amazon.',
	)
	description = models.TextField(null=True, blank=True)
	categories = models.ManyToManyField(BookCategory, blank=True)
	book_image = models.ImageField(upload_to='book-covers/')
	

	is_active_category = models.BooleanField(
		default=False,
		help_text='Is it displayed on category page?')

	is_highlighted_category = models.BooleanField(
		default=False,
		help_text='Is it highlighted on main page?'
	)
	
	is_active_main = models.BooleanField(
		default=False,
		help_text='Is it displayed on main page?'
	)
	is_highlighted_main = models.BooleanField(
		default=False,
		help_text='Is it highlighted on main page?'
	)

	has_audiobook = models.BooleanField(null=True, blank=True, default=False)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


	def get_publication_year(self):
		if self.publication_date:
			return self.publication_date.year
		else:
			return None

	def __str__(self):
		return self.title


class AmazonReferralLink(models.Model):
	"""
	Amazon reference link model.
	Will be used to generate full links in templates.
	"""
	amazon_referral_url = models.CharField(
		max_length=200,
		help_text='Referral part of the link only (without https://www.amazon.com/',
	)

	def __str__(self):
		return self.amazon_referral_url