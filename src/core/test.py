from datetime import datetime
import time
import pandas as pd

raw_date = 'Mon, 25 Jun 2018 13:30:27 +0000'

# print(time.mktime(raw_date))
print(pd.to_datetime(raw_date))
# print(datetime.fromtimestamp)

# print([{'value': ''}])[0]['value'])
article = {'content': 'sdd'}
c = article.get(
			'content', [{'value': ''}])[0]['value']

print(c)