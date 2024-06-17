import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrap_article(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article')

    texts = []
    for article in articles:
        title = article.find('h1', class_='post-title').text
        content = ""
        paragraphs = article.find_all('p', class_='text-align-justify')
        for paragraph in paragraphs:
            content += paragraph.text
        texts.append(f"{title}\n{content}")

    return texts


url = 'https://www.urania.edu.pl/wiadomosci/pokaz-mozliwosci-wielkiego-teleskopu-lornetkowego'
texts = scrap_article(url)

data = {'text': texts, 'label': 'astronomia'}
df = pd.DataFrame(data)
df.to_csv('articles_data.csv', index=False)