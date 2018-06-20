from django.shortcuts import render


def home_view(request):
	template = 'home.html'
	context = {}

	return render(request, template, context)
