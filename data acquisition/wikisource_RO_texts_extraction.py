import os
import ebooklib
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import urllib.parse

"""

STILL THINKING HOW TO DO IT!!!!!
(wikisource is kinda strange to work with)

"""


def decode_url_title(encoded_html_href):
    decoded_title = urllib.parse.unquote(encoded_html_href).replace("/wiki/", "")
    return decoded_title.replace('_', ' ')

def search_texts(author_name):
    author_page = f"https://ro.wikisource.org/wiki/Autor:{author_name}"
    response = requests.get(author_page)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_titles = []

        for html_ul_elem in soup.find_all('ul'):
            for html_li_elem in html_ul_elem.find_all('li'):
                html_a_elem = html_li_elem.find('a')
                if html_a_elem:
                    text_title = html_a_elem.text.strip()
                    encoded_html_href_title = html_a_elem['href']
                    decoded_title = decode_url_title(encoded_html_href_title)

                    if decoded_title == text_title:
                        link_to_book = f"https://ro.wikisource.org{html_a_elem['href']}"
                        print(f"Title: {text_title}, Link: {link_to_book}")
                        text_titles.append(link_to_book)

        print("Text titles found:")
        for title in text_titles:
            print(title)

        return text_titles

    else:
        print(f"Error accessing page: {response.status_code}")
        return []


name = input("Author name: ")
all_text_titles = search_texts(name)
