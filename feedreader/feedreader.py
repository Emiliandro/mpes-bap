!pip install feedparser

import feedparser as fp
import re
import json
from datetime import date
from datetime import datetime
from dateutil.parser import parse


"""## Removing HTML Tags"""

CLEANR = re.compile('<.*?>')

def doHTMLcleanning(raw_html):
  return re.sub(CLEANR,'',raw_html)

"""# Creating the MVP"""

messages_generated = []
today = str((date.today()).strftime("%m/%d/%Y"))

class RawMessage:
  def __init__(self, summary, timestamp, url, tag):
    self.summary = summary
    self.timestamp = timestamp
    self.url = url
    self.tag = tag

  def toJson(self): 
    return json.dumps(self, default=lambda o: o.__dict__)

references = {
    'autoesporte':['http://g1.globo.com/dynamo/carros/rss2.xml','https://noticias.r7.com/carros/feed.xml','https://esportes.r7.com/automobilismo/feed.xml'],
    'tecnologia':['http://g1.globo.com/dynamo/tecnologia/rss2.xml', 'https://noticias.r7.com/tecnologia-e-ciencia/feed.xml'],
    'economia':['http://g1.globo.com/dynamo/economia/rss2.xml','https://noticias.r7.com/economia/feed.xml', 'https://br.investing.com/rss/forex_Opinion.rss','https://br.investing.com/rss/market_overview_Opinion.rss'],
    'turismo':['http://g1.globo.com/dynamo/turismo-e-viagem/rss2.xml', 'https://lifestyle.r7.com/viagens/feed.xml']
}

for key, value in references.items() :
    print (key, value)

def check_results(request_result, tag):
  for i in request_result['entries']:
    item_time = (i['published'])
    date_str = parse(item_time).strftime("%m/%d/%Y")
    message_to_be_send = RawMessage(i['title'],date_str,i['link'],tag)
    messages_generated.append(message_to_be_send)

def check_url_array(key_from_dic, tag):
  for url_from_dic in key_from_dic:
    request_fp_parte = fp.parse(url_from_dic)
    check_results(request_fp_parte,tag)

for key, value in references.items() :
  check_url_array(value, str(key))

for msg in messages_generated:
    print(msg.tag, msg.summary, msg.timestamp, msg.url)