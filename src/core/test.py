"""
from datetime import datetime
import time
import pandas as pd

raw_date = 'Mon, 25 Jun 2018 13:30:27 +0000'
pd_date =  pd.to_datetime(raw_date)
datetime_date = datetime.fromtimestamp(pd_date)
# print(time.mktime(raw_date))
print(pd.to_datetime(raw_date))
# print(datetime.fromtimestamp)

# print([{'value': ''}])[0]['value'])
article = {'content': 'sdd'}



# print(datetime.fromtimestamp(time.mktime(raw_date)))
print(pd_date)
print(datetime_date)
"""

desc = """
<p>Introduction I am incredibly proud to announce the launch of DataHack Radio! This is Analytics Vidhya&#8217;s exclusive podcast series which will feature top leaders ... </p>
<p>The post <a rel="nofollow" href="https://www.analyticsvidhya.com/blog/2018/06/launching-datahack-radio-analytics-vidhyas-exclusive-podcast-series/">Launching DataHack Radio &#8211; Analytics Vidhya&#8217;s Exclusive Podcast Series!</a> appeared first on <a rel="nofollow" href="https://www.analyticsvidhya.com">Analytics Vidhya</a>.</p>
"""



# import bs4 as BeautifulSoup
from bs4 import BeautifulSoup
tag = '- sometag -'

def normalize_tag(tag):
	""" Converts "- sometag -" to "tag" and "some tag" to some-tag"""
	tag = tag.strip('-')
	# Fix for HTML entities
	tag = BeautifulSoup(tag, 'html.parser').prettify()
	tag = tag.strip().lower()
	tag = tag.replace(' ', '-')
	return tag


def normalize_description(description):
	""" Cleaning form html tags """
	description = BeautifulSoup(description, 'html.parser').get_text()
	return description


print(normalize_description(desc))
