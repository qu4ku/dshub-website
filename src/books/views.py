from django.shortcuts import render

# Create your views here.
def books_view(request):
	context = {}
	template = 'books.html'

	return render(request, template, context)