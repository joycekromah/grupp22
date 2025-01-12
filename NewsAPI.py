
import requests
from dotenv import load_dotenv
import json
import os

# Load environment variables from the .env file
load_dotenv()

def main(searchWord):
    """
    Fetch articles for the given search word and return them as JSON objects.
    """
    posts = get_articles(searchWord)
    if posts:
        articles = [
            {"title": article.get("title", "No title available"), "url": article.get("url", "No URL available")}
            for article in posts.get("articles", [])
        ]
        for article in articles:
            print(article)

        return articles
    return []

def get_articles(searchWord):
    # Retrieve the API key from the environment variables
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        print("Error: API key not found. Make sure it's set in the .env file.")
        return None

    url = f'https://newsapi.org/v2/everything?q={searchWord}&pageSize=10&apiKey={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        posts = response.json()
        return posts
    else:
        print(f"Error: {response.status_code}")
        return None