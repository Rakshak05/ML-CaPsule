import webbrowser
import urllib.parse
import xml.etree.ElementTree as ET
import requests
import wikipedia
from Voice_CLI_Virtual_Assistant import config

def get_wikipedia_summary(query: str, sentences: int = 2) -> str:
    """Fetch summary from Wikipedia."""
    try:
        # Search for the query first to get the best matching title
        search_results = wikipedia.search(query)
        if not search_results:
            return "No matching Wikipedia articles found."
        
        # Get summary of the first result
        summary = wikipedia.summary(search_results[0], sentences=sentences)
        return f"According to Wikipedia: {summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        # If ambiguous, try the first option
        try:
            summary = wikipedia.summary(e.options[0], sentences=sentences)
            return f"According to Wikipedia: {summary}"
        except Exception:
            return f"The search term is too ambiguous. Options include: {', '.join(e.options[:3])}."
    except wikipedia.exceptions.PageError:
        return f"Could not find any page matching '{query}' on Wikipedia."
    except Exception as e:
        return f"An error occurred while fetching from Wikipedia: {e}"

def search_google(query: str):
    """Launch Google Search in default browser."""
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)
    return f"Searching Google for: {query}"

def play_youtube(query: str):
    """Launch YouTube search or attempt to open direct query in browser."""
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(url)
    return f"Opening YouTube results for: {query}"

def get_weather(city: str = config.DEFAULT_WEATHER_CITY) -> str:
    """Fetch real-time localized weather indexing from wttr.in."""
    try:
        # Fetching JSON format from wttr.in
        url = f"https://wttr.in/{city}?format=j1"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current_condition = data['current_condition'][0]
            temp_c = current_condition['temp_C']
            weather_desc = current_condition['weatherDesc'][0]['value']
            humidity = current_condition['humidity']
            windspeed = current_condition['windspeedKmph']
            
            return (f"The current weather in {city} is {temp_c}°C with {weather_desc}. "
                    f"Humidity is {humidity}% and wind speed is {windspeed} kilometers per hour.")
        else:
            # Fallback to plain text format
            text_response = requests.get(f"https://wttr.in/{city}?format=3", headers=headers, timeout=10)
            if text_response.status_code == 200:
                return f"Weather in {city}: {text_response.text.strip()}"
            return "Could not retrieve weather details at this moment."
    except Exception as e:
        return f"Failed to retrieve weather data: {e}"

def get_top_news(limit: int = 5) -> list:
    """Fetch top news headlines from Google News RSS feed."""
    news_headlines = []
    try:
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('./channel/item')[:limit]:
                title = item.find('title').text
                # Remove source trailing name (e.g. " - Times of India") if present
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                news_headlines.append(title)
        else:
            news_headlines.append("Could not fetch news headlines right now.")
    except Exception as e:
        news_headlines.append(f"Failed to load headlines: {e}")
        
    return news_headlines
