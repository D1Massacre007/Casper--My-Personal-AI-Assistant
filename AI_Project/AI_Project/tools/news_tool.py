# AI_Project/tools/news_tool.py
import os
import requests

class NewsTool:
    def __init__(self):
        self.api_key = os.environ.get('NEWS_API_KEY')

    def fetch_headlines(self, query: str = 'top', country: str = 'us'):
        if self.api_key and self.api_key != 'REPLACE_ME':
            url = 'https://newsapi.org/v2/top-headlines'
            params = {'apiKey': self.api_key, 'pageSize': 10, 'country': country}
            if query and query != 'top':
                params['q'] = query
            r = requests.get(url, params=params, timeout=10)
            data = r.json()
            if data.get('status') != 'ok':
                return 'News API error: ' + str(data)
            return '\n'.join([f"{i+1}. {a['title']} ({a['source']['name']})" for i,a in enumerate(data.get('articles',[]))])
        else:
            # fallback: use CNN RSS for headlines
            try:
                rss = 'https://rss.cnn.com/rss/edition.rss'
                r = requests.get(rss, timeout=10)
                items = r.text.split('<item>')[1:6]
                headlines = []
                for it in items:
                    try:
                        title = it.split('<title>')[1].split('</title>')[0]
                        headlines.append(title)
                    except Exception:
                        continue
                return '\n'.join(headlines)
            except Exception as e:
                return 'Failed to fetch headlines: ' + str(e)

    def run(self, q: str):
        return self.fetch_headlines(q)
