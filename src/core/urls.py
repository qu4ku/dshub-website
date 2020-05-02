from django.urls import path
from django.conf.urls import handler404

from . import views


handler404 = 'core.views.handler404_view'


urlpatterns = [
	path('', views.home_view, name='home'),
	path('about/', views.about_view, name='about'),
	path('tags/', views.tags_list_view, name='tags_list'),
	path('other-tags/', views.other_tags_list_view, name='other_tags_list'),
	path('tag/<slug:slug>/', views.tag_view, name='tag'),
	path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
	path('results/', views.search_view, name='search'),
]
