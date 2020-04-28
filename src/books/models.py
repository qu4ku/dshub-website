from django.db import models

# Create your models here.
class BookCategory(models.Model):
	"""
	BookCategory model. 

	Works as a category of a book but aslo as more general model for category subpage.
	"""

	class Meta:
		verbose_name = 'Book Category'
		verbose_name_plural = 'Book Categories'
		db_table = 'book_category'
		ordering = ('title',)

	# Do not turn it off once is on: seo
	is_active = models.BooleanField(default=False)
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# Used to generate subpage
	headline = models.CharField(max_length=200, null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	# Seo
	seo_title = models.CharField(max_length=60, blank=True, null=True)
	seo_description = models.CharField(max_length=165, blank=True, null=True)


	def __str__(self):
		return self.title
	
	# def get_absolute_url(self):
	# 	return reverse("model_detail", kwargs={"pk": self.pk})
	

class Book(models.Model):

	class Meta:
		verbose_name = 'Book'
		verbose_name_plural = 'Books'
		db_table = 'book'
		ordering = ('is_highlighted_category', 'title',)

	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200, null=True, blank=True)
	rating_good_reads = models.CharField(max_length=10, null=True, blank=True, default='NA')
	rating_amazon = models.CharField(max_length=10, null=True, blank=True, default='NA')
	description = models.TextField(null=True, blank=True)
	url = models.URLField(
		max_length=250,
		help_text='Url to amazon.',
	)

	category = models.ManyToManyField(BookCategory, blank=True)
	
	is_active = models.BooleanField(
		default=False,
		help_text='Is it displayed on main page?')
	
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


	def __str__(self):
		return self.title