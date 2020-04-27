from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from .sitemaps import PostsSitemap, TagsSitemap, StaticSitemap, HomeSitemap


sitemaps = {
	'posts': PostsSitemap,
	'tags': TagsSitemap,
	'pages': StaticSitemap,
	'home': HomeSitemap,
}

urlpatterns = [
	path('my_admin/', admin.site.urls),
	path('', include('core.urls')),
	path('books/', include('books.urls')),
	path('sitemap.xml', sitemap, {'sitemaps': sitemaps})
]


if settings.DEBUG:
	import debug_toolbar
	urlpatterns = [
		path('__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)