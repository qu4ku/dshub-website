import feedparser

f = feedparser.parse('https://www.kdnuggets.com/feed')
print(f['feed']['title'])