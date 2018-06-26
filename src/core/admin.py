from django.contrib import admin
from .models import Post, Feed, Tag


admin.site.register(Post)
admin.site.register(Feed)
admin.site.register(Tag)
