
import feedparser as fp
import re
import json
from datetime import date
from datetime import datetime
from dateutil.parser import parse


CLEANR = re.compile('<.*?>')
def doHTMLcleanning(raw_html):
  return re.sub(CLEANR,'',raw_html)

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
    'autoesporte':[
      'http://g1.globo.com/dynamo/carros/rss2.xml',
      'https://noticias.r7.com/carros/feed.xml',
      'https://esportes.r7.com/automobilismo/feed.xml'
      ],
    'tecnologia':[
      'http://g1.globo.com/dynamo/tecnologia/rss2.xml', 
      'https://noticias.r7.com/tecnologia-e-ciencia/feed.xml'
      ],
    'economia':[
      'http://g1.globo.com/dynamo/economia/rss2.xml',
      'https://noticias.r7.com/economia/feed.xml', 
      'https://br.investing.com/rss/forex_Opinion.rss',
      'https://br.investing.com/rss/market_overview_Opinion.rss'],
    'turismo':[
      'http://g1.globo.com/dynamo/turismo-e-viagem/rss2.xml', 
      'https://lifestyle.r7.com/viagens/feed.xml'
      ]
}

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

def get_if_contain(search_for):
  is_in = False
  values_to_search = []
  result = []
  
  for key, value in references.items() :
    if (key == search_for): 
      is_in = True
      values_to_search = value
      break

  if (is_in): 
    check_url_array(values_to_search,search_for)
    result = messages_generated
  
  return result

def get_categories():
  options = []
  for key, value in references.items() :
    options.append(key)
  return options