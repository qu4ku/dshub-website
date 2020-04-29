from django.urls import path

from . import views


urlpatterns = [
	path('', views.books_view, name='books'),
	path('<slug:slug>/', views.book_category_view, name='book_category'),
]