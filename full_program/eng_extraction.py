# eng_extraction.py

import os
import ebooklib
import requests
from bs4 import BeautifulSoup
from ebooklib import epub

class EnglishTextExtractor:
    def __init__(self, author_name, output_directory, logger=None):
        self.author_name = author_name
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        if logger is None:
            self.logger = print
        else:
            self.logger = logger

    def search_epub(self):
        self.logger(f"Searching for EPUB files for author {self.author_name}...")
        # The search url for author name
        search_url = f'https://www.gutenberg.org/ebooks/search/?query={self.author_name}&submit_search=Go%21'
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract EPUB links
        epub_links = []
        for book in soup.find_all('li', class_='booklink'):
            link_tag = book.find('a', href=True)
            if not link_tag:
                continue
            book_url = f'https://www.gutenberg.org{link_tag["href"]}'

            book_page = requests.get(book_url)
            book_soup = BeautifulSoup(book_page.text, 'html.parser')

            for link in book_soup.find_all('a', href=True):
                if 'epub.noimages' in link['href']:
                    epub_link = f'https://www.gutenberg.org{link["href"]}'
                    epub_links.append(epub_link)
                    break

        self.logger(f"Found {len(epub_links)} EPUB files for author {self.author_name}.")
        return epub_links

    def download_epub(self, epub_url, output_path):
        self.logger(f"Downloading EPUB file from {epub_url}...")
        response = requests.get(epub_url)
        with open(output_path, 'wb') as epub_file:
            epub_file.write(response.content)
        self.logger(f"Downloaded: {output_path}")

    def epub_to_txt(self, epub_file_path, output_txt_path):
        self.logger(f"Converting {epub_file_path} to text...")
        book = epub.read_epub(epub_file_path)
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_body_content().decode('utf-8')
                    soup = BeautifulSoup(content, 'html.parser')
                    txt_file.write(soup.get_text())
        self.logger(f"Converted {epub_file_path} to {output_txt_path}")

    def get_title_from_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if "Title:" in line:
                    return line.split("Title:")[1].strip()
        return None

    def clean_text_content(self, file_path, output_path):
        start_marker = "*** START OF"
        end_marker = "*** END OF"
        content_started = False

        with open(file_path, 'r', encoding='utf-8') as file, open(output_path, 'w', encoding='utf-8') as out_file:
            for line in file:
                if start_marker in line:
                    content_started = True
                    continue
                if end_marker in line:
                    break
                if content_started:
                    out_file.write(line)
        self.logger(f"Cleaned and saved file: {output_path}")

    def rename_and_clean_files(self, directory):
        for file_name in os.listdir(directory):
            if file_name.endswith('.txt'):
                file_path = os.path.join(directory, file_name)

                title = self.get_title_from_text(file_path)
                if not title:
                    self.logger(f"Could not find title in {file_name}, skipping.")
                    continue

                sanitized_title = "".join(c for c in title if c.isalnum() or c in (' ', '.', '_')).rstrip()
                new_file_name = f"{sanitized_title}.txt"
                new_file_path = os.path.join(directory, new_file_name)
                self.clean_text_content(file_path, new_file_path)

                os.remove(file_path)
                self.logger(f"Renamed {file_name} to {new_file_name} and cleaned it.")

    def delete_epubs(self, directory):
        for file_name in os.listdir(directory):
            if file_name.endswith('.epub'):
                file_path = os.path.join(directory, file_name)
                os.remove(file_path)
                self.logger(f"Deleted {file_name}")

    def extract(self):
        epub_links = self.search_epub()

        if not epub_links:
            self.logger(f"No EPUB files found for author {self.author_name}.")
            return

        author_dir = os.path.join(self.output_directory, self.author_name)
        if not os.path.exists(author_dir):
            os.makedirs(author_dir)

        for i, epub_link in enumerate(epub_links):
            epub_file_path = os.path.join(author_dir, f'{self.author_name}_{i}.epub')
            txt_file_path = os.path.join(author_dir, f'{self.author_name}_{i}.txt')

            self.download_epub(epub_link, epub_file_path)
            self.epub_to_txt(epub_file_path, txt_file_path)

        self.rename_and_clean_files(author_dir)
        self.delete_epubs(author_dir)
