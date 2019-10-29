from django.contrib import admin

from .models import Post, Feed, Tag, OtherTag


class PostAdmin(admin.ModelAdmin):

	class Meta:
		model = Post

	list_display = ['feed', 'title', 'date', 'is_active']
	list_editable = ['is_active']
	list_filter = ['is_active', 'feed', 'tags', 'other_tags']
	search_fields = ['title', 'content']


class FeedAdmin(admin.ModelAdmin):

	class Meta:
		model = Feed

	list_display = ['title', 'is_active']
	list_editable = ['is_active']

admin.site.register(Post, PostAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Tag)
admin.site.register(OtherTag)
