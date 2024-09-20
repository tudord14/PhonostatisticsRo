import os
import ebooklib
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import urllib.parse
from bs4.element import Tag
import re

"""

STILL THINKING HOW TO DO IT!!!!!
(wikisource is kinda strange to work with)

UPDATE: 20.09 ->
        -> the code obtains the texts from a specific romanian author
        but the folder is not really "clean"
        -> a follow up program for cleaning the folder will be created
        ->(I hope it will happen soon)

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
                        text_titles.append(link_to_book)
        return text_titles[1:]
    else:
        print(f"Error accessing page: {response.status_code}")
        return []


def get_text_from_html(text_links):
    texts = []
    for link in text_links:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_title = link.replace("https://ro.wikisource.org/wiki/", "")

            # The text is usually contained into the html div elemnt
            # <div class="mw-content-ltr mw-parser-output" lang="ro" dir="ltr">
            content_div = soup.find('div', class_='mw-parser-output')
            if content_div:
                for span in content_div.find_all('span'):
                    span.decompose()

                text_content = ""
                for child in content_div.children:
                    if isinstance(child, Tag) and child.name != 'span':
                        text_content += child.get_text(separator="\n", strip=True) + "\n"

                texts.append({'title': text_title, 'content': text_content})
            else:
                print(f"Content div not found {link}")
        else:
            print(f"Error when trying to access page: {response.status_code}")
    return texts


def transform_texts_to_txt(texts, author_name):
    os.makedirs(author_name, exist_ok=True)

    for text in texts:
        title = urllib.parse.unquote(text['title'])
        content = text['content']
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", title)
        file_path = os.path.join(author_name, f"{sanitized_title}.txt")

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Saved '{title}' to '{file_path}'")

name = input("Author name: ")
all_text_titles = search_texts(name)
texts = get_text_from_html(all_text_titles)
transform_texts_to_txt(texts, name)
