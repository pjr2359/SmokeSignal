import requests
from django.core.cache import cache
import urllib.parse
from datetime import datetime, timedelta

class GDELTNewsService:
    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
    
    @staticmethod
    def get_cannabis_news(limit=3):
        cache_key = 'cannabis_news'
        cached_news = cache.get(cache_key)
        
        if cached_news:
            return cached_news
            
        query_params = {
            'query': 'cannabis OR marijuana',
            'mode': 'artlist',
            'format': 'json',
            'maxrecords': limit,
            'timespan': '24h',
            'sort': 'DateDesc'
        }
        
        url = f"{GDELTNewsService.BASE_URL}?{urllib.parse.urlencode(query_params)}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                articles = response.json()['articles']
                return articles
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []