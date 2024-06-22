import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

def scrap_article(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content_div = soup.find('div', class_='post-content')
    if content_div:
        return content_div.get_text()
    else:
        return ''

def scrap_page(page_url, main_page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_links = soup.find_all('a', rel='bookmark')

    links = []
    for link in article_links:
        article_url = link['href']
        if not article_url.startswith('https'):
            article_url = main_page_url + article_url
        links.append(article_url)

    return links

def scrap_all_pages(base_url, main_page_url, max_pages=5):

    articles = []

    for page in range(0, max_pages):
        page_url = f"{base_url}?page={page}"
        article_links = scrap_page(page_url, main_page_url)
    
        for link in article_links:
            article_content = scrap_article(link)
            articles.append(article_content)

            time.sleep(1)

    return articles

urania_url = 'https://www.urania.edu.pl'
urania_astronomia_url = 'https://www.urania.edu.pl/taxonomy/term/3096'
articles_urania = scrap_all_pages(urania_astronomia_url, urania_url)

data = {'text': articles_urania, 'label': 'astronomia'}
df = pd.DataFrame(data)
df.to_csv('articles_data.csv', index=False)