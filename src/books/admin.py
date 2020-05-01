from django.contrib import admin

from .models import Book, BookCategory, AmazonReferralLink


class BookAdmin(admin.ModelAdmin):

	class Meta:
		model = Book

	list_display = ['title', 'author']
	# list_editable = ['is_active']
	# list_filter = ['is_active', 'feed', 'tags', 'other_tags']
	# search_fields = ['title', 'content']


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(BookCategory)
admin.site.register(AmazonReferralLink)