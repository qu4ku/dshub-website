from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, BookCategory

def books_view(request):
	context = {}
	template = 'books.html'

	return render(request, template, context)


def book_category_view(request, slug):
	template = 'book-category.html'

	category_obj = get_object_or_404(BookCategory, slug=slug, is_active=True)

	books = Book.objects.filter(categories=category_obj)
	
	if books:
		context = {
			'books': books,
			'category': category_obj,
		}

	return render(request, template, context)


