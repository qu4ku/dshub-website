from django.contrib import admin

from .models import Post, Feed, Tag, OtherTag


class PostAdmin(admin.ModelAdmin):

	class Meta:
		model = Post

	list_filter = ['is_active', 'feed', 'tags', 'other_tags']
	search_fields = ['title', 'content']


admin.site.register(Post, PostAdmin)
admin.site.register(Feed)
admin.site.register(Tag)
admin.site.register(OtherTag)
