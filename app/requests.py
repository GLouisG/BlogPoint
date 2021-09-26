import urllib.request,json
from .models import Quotes

base_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def find_quotes(info):

  with urllib.request.urlopen(base_url) as url:
    get_quote_data = url.read()
    get_quote_response=json.loads(get_quote_data)


    if get_quote_response:
      author = get_quote_response.get('author')
      quote = get_quote_response.get('quote')
      quote_obj = Quotes(author, quote)
  return quote_obj  