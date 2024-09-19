import os
import ebooklib
import requests
from bs4 import BeautifulSoup
from ebooklib import epub


def transform_title(text_title):
    return text_title.strip()


def search_texts(author_name):
    author_page = f"https://ro.wikisource.org/wiki/Autor:{author_name}"
    response = requests.get(author_page)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_titles = []

        for book in soup.find_all('a', href=True):
            text_title = book.text
            link_to_book = book['href']

            text_titles.append(text_title)

        print("Text titles found:")
        for title in text_titles:
            print(title)

        return text_titles

    else:
        print(f"Error accessing page: {response.status_code}")
        return []


name = input("Author name: ")
all_text_titles = search_texts(name)
