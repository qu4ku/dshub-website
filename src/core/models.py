from django.db import models


class Feed(models.Model):
	"""Feed model of the source website."""

	class Meta:
		verbose_name = 'Feed'
		verbose_name_plural = 'Feeds'
		ordering = ('title', )
		db_table = 'feed'

	title = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	# URL to the website
	url = models.URLField(max_length=250)
	# URL to the feed
	url_feed = models.URLField(max_length=250)
	# URL in human friendly format
	url_display = models.CharField(max_length=250)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	# If not active feed won't be followed
	is_active = models.BooleanField(default=True)

	# Optional
	author = models.CharField(max_length=100, blank=True)
	description = models.TextField(null=True, blank=True)
	seo_title = models.CharField(max_length=60, blank=True, null=True)
	seo_description = models.CharField(max_length=165, blank=True, null=True)

	def __str__(self):
		return self.title


class Tag(models.Model):
	"""Tag model. Many to many."""

	class Meta:
		verbose_name = 'Tag'
		verbose_name_plural = 'Tags'
		db_table = 'tag'
		ordering = ('title',)

	title = models.CharField(max_length=100, blank=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	seo_title = models.CharField(max_length=60, blank=True, null=True)
	seo_description = models.CharField(max_length=165, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return '/tag/{}/'.format(self.slug)


class OtherTag(models.Model):
	"""OtherTag model for tags that are not in the database already."""

	class Meta:
		verbose_name = 'Other Tag'
		verbose_name_plural = 'Other Tags'
		db_table = 'other_tag'
		ordering = ('title',)

	title = models.CharField(max_length=100, blank=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	seo_title = models.CharField(max_length=60, blank=True, null=True)
	seo_description = models.CharField(max_length=165, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.slug


class Post(models.Model):
	""" Post model."""

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'
		db_table = 'post'
		ordering = ('-date',)
		get_latest_by = 'date'


	is_active = models.BooleanField(default=True)
	is_hidden = models.BooleanField(default=False)
	title = models.CharField(max_length=280)
	source_url = models.URLField(
		max_length=250,
		help_text="URL of the original article.",
	)
	content = models.TextField(null=True, blank=True)
	feed = models.ForeignKey(Feed, null=True, on_delete=models.SET_NULL)
	guid = models.CharField(max_length=32)
	slug = models.SlugField(max_length=280)
	date = models.DateTimeField(
		help_text="When this post says it was published.",
	)
	tags = models.ManyToManyField(Tag, blank=True)
	other_tags = models.ManyToManyField(OtherTag, blank=True)
	

	def __str__(self):
		return '{} | {}'.format(self.feed.title, self.title)

	def get_absolute_url(self):
		return '/post/{}/'.format(self.slug)