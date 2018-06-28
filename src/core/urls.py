from django.urls import path

from . import views


urlpatterns = [
	path('', views.home_view, name='home'),
	path('about/', views.about_view, name='about'),
	path('tags/', views.tags_list_view, name='tags_list'),
	path('tag/<slug:slug>', views.tag_view, name='tag'),
	path('run/', views.run_view, name='run'),
]