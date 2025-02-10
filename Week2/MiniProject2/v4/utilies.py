import requests
from config import API_KEY, BASE_URL

def get_weather_data(city_name):
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def get_youtube_url(url):
    ydl_opts = {'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']
        