
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def main():
    searchWord = input("Ange sökord: ")
    posts = get_articles(searchWord)
    if posts:
        format_output(posts)


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


def format_output(posts):
    articles = posts.get('articles', [])
    for article in articles:
        url = article.get('url', 'No content available')
        print(url)


if __name__ == '__main__':
    main()
