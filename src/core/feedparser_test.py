import feedparser
import hashlib
from .models import Post, Feed

feed_url = 'https://www.kdnuggets.com/feed'
feed = feedparser.parse(feed_url)

articles = feed['items']

for article in articles[:8]:
	print(article['published'])
	print(article.get('published'))

	title = article.get('title')
	date = article.get('published')
