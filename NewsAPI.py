import requests

def main():
    searchWord = input("Ange sökord: ")
    posts = get_articles(searchWord)
    format_output(posts)


def get_articles(searchWord):

     url = f'https://newsapi.org/v2/everything?q={searchWord}&pageSize=10&apiKey=7113466387ef4dc29321b66a334c094f'

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