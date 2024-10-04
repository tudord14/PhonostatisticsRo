import os
import requests
from bs4 import BeautifulSoup, Tag
import urllib.parse
import re

class RomanianTextExtractor:
    def __init__(self, author_name, output_directory, logger=None):
        self.author_name = author_name
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        if logger is None:
            self.logger = print
        else:
            self.logger = logger

    def decode_url_title(self, encoded_html_href):
        decoded_title = urllib.parse.unquote(encoded_html_href).replace("/wiki/", "")
        return decoded_title.replace('_', ' ')

    def search_texts(self):
        self.logger(f"Searching for texts by {self.author_name}...")
        author_page = f"https://ro.wikisource.org/wiki/Autor:{self.author_name}"
        response = requests.get(author_page)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_titles = []

            for html_ul_elem in soup.find_all('ul'):
                for html_li_elem in html_ul_elem.find_all('li'):
                    html_a_elem = html_li_elem.find('a')
                    if html_a_elem:
                        # Skip <a> elements with color #D73333
                        style = html_a_elem.get('style', '')
                        if 'color:#D73333' in style.replace(' ', ''):
                            continue

                        text_title = html_a_elem.text.strip()
                        encoded_html_href_title = html_a_elem['href']
                        decoded_title = self.decode_url_title(encoded_html_href_title)

                        if decoded_title == text_title:
                            link_to_book = f"https://ro.wikisource.org{html_a_elem['href']}"
                            text_titles.append(link_to_book)
            self.logger(f"Found {len(text_titles)} texts for {self.author_name}.")
            return text_titles[1:]
        else:
            self.logger(f"Error accessing page: {response.status_code}")
            return []

    def get_text_from_html(self, text_links):
        texts = []
        for link in text_links:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text_title = link.replace("https://ro.wikisource.org/wiki/", "")
                text_title = urllib.parse.unquote(text_title).replace('_', ' ')

                content_div = soup.find('div', class_='mw-parser-output')
                if content_div:
                    for tag in content_div.find_all(['span', 'td', 'a', 'div']):
                        tag.decompose()

                    text_content = ""
                    for child in content_div.children:
                        if isinstance(child, Tag):
                            text_content += child.get_text(separator="\n", strip=True) + "\n"

                    texts.append({'title': text_title, 'content': text_content})
                    self.logger(f"Retrieved text: {text_title}")
                else:
                    self.logger(f"Content div not found for {link}")
            else:
                self.logger(f"Error accessing page {link}: {response.status_code}")
        return texts

    def transform_texts_to_txt(self, texts):
        author_dir = os.path.join(self.output_directory, self.author_name)
        os.makedirs(author_dir, exist_ok=True)

        for text in texts:
            title = urllib.parse.unquote(text['title'])
            content = text['content']
            sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", title)
            file_path = os.path.join(author_dir, f"{sanitized_title}.txt")

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            self.logger(f"Saved '{title}' to '{file_path}'")

    def extract(self):
        text_links = self.search_texts()
        if not text_links:
            self.logger(f"No texts found for author {self.author_name}.")
            return

        texts = self.get_text_from_html(text_links)
        self.transform_texts_to_txt(texts)
