
import requests
from dotenv import load_dotenv
import json
import os

# Load environment variables from the .env file
load_dotenv()

def main():
    searchWord = input("Ange sökord: ")
    posts = get_articles(searchWord)
    if posts:
        save_urls_as_json(posts)


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


def save_urls_as_json(posts):
    articles = posts.get('articles', [])
    urls = [{"title": article.get('title', 'No title available'), "url": article.get('url', 'No URL available')} for article in articles]

    # Save URLs as JSON
    with open('articles.json', 'w', encoding='utf-8') as json_file:
        json.dump(urls, json_file, indent=2, ensure_ascii=False)

    print("URLs have been saved to 'articles.json'.")


if __name__ == '__main__':
    main()
