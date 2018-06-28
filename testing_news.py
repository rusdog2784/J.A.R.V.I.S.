import requests

api_key = '603fdd9223614b60826a80b8ad29afa8'
#url = ('https://newsapi.org/v2/top-headlines?'
#       'country=us&'
#       'apiKey=' + api_key)
#source = 'google-news'
#source = 'bloomberg'
source = 'the-verge'
search = 'headphones'
url = ('https://newsapi.org/v2/top-headlines?'
        'sources=' + source +
#        'q=' + search +
        '&apiKey=' + api_key)
response = requests.get(url)
#print response.json()

result_json = response.json()
results = result_json['articles']
for result in results:
    print(result['title'])
    print(result['url'])
    print(result['publishedAt'])
    print(result['source']['name'])
    print('-'*60)