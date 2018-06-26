from django.db import models


class Feed(models.Model):

	title = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	url = models.URLField(max_length=250)
	url_display = models.CharField(max_length=250)

	author = models.CharField(max_length=100, blank=True)
	description = models.TextField(null=True, blank=True)
	seo_title = models.CharField(max_length=60, blank=True, null=True)
	seo_description = models.CharField(max_length=165, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Feed'
		verbose_name_plural = 'Feeds'
		ordering = ('title', )
		db_table = 'feed'

	def __str__(self):
		return self.title


class Tag(models.Model):

	title = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	seo_title = models.CharField(max_length=60, blank=True, null=True)
	seo_description = models.CharField(max_length=165, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Tag'
		verbose_name_plural = 'Tags'
		db_table = 'tag'
		ordering = ('title',)

	def __str__(self):
		return self.title



class Post(models.Model):

	STATUS_CHOICES = (
		('draft', 'Draft'),
		('public', 'Public'),
	)

	feed = models.ForeignKey(Feed, null=True, on_delete=models.SET_NULL)

	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='public')

	# Compulsory fields
	title = models.CharField(max_length=280)
	source_url = models.URLField(
		max_length=250,
		help_text="URL for original article.",
	)

	content = models.TextField(null=True, blank=True)
	date = models.DateTimeField(
		help_text="When this post says it was published.",
	)


	is_active = models.BooleanField(default=True)
	guid = models.CharField(max_length=32)

	tags = models.ManyToManyField(Tag, blank=True)

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'
		db_table = 'post'
		ordering = ('-date', )
		get_latest_by = 'date'

	def __str__(self):
		# return '{} | {}'.format(self.feed.title, self.title)
		return self.title



