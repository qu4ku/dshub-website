import django
from django.conf import settings
from stro
django.setup()


import feedparser
import hashlib

from models import Post, Feed
# from test import ADAM
# from . import models
# import models

print(ADAM)

feed_url = 'https://www.kdnuggets.com/feed'
feed = feedparser.parse(feed_url)

articles = feed['items']
print(len(articles))
# for article in articles[:8]:
# 	print(article['published'])
# 	print(article.get('published'))

# 	title = article.get('title')
# 	date = article.get('published')
# 	source_url = article.get('link')
