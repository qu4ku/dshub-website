from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Book, BookCategory

def books_view(request):
	context = {}
	template = 'books.html'

	return render(request, template, context)


def books_view(request):
	template = 'books.html'

	books = Book.objects.filter(is_active_main=True)
	categories = BookCategory.objects.filter(is_active=True)
	
	context = {
		'books': books,
		'categories': categories,
	}

	return render(request, template, context)


def book_category_view(request, slug):
	template = 'book-category.html'

	category_obj = get_object_or_404(BookCategory, slug=slug, is_active=True)
	books = Book.objects.filter(categories=category_obj, is_active_category=True)

	categories = BookCategory.objects.filter(is_active=True).exclude(slug=category_obj.slug)
	
	if books:
		context = {
			'books': books,
			'category': category_obj,
			'categories': categories,
		}
		return render(request, template, context)
	else:
		# The case when the category is active but no books found
		return HttpResponseRedirect(reverse('books'))

	


