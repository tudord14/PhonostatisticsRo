import string
import pandas as pd
import unicodedata
import os
import re
import math
import nltk
from nltk.util import ngrams
from collections import defaultdict, Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
nltk.download('punkt')

def get_texts_from_folder(directory):
    text_files = []

    for author in os.listdir(directory):
        author_directory = os.path.join(directory, author)

        if os.path.isdir(author_directory):
            for file in os.listdir(author_directory):
                if file.endswith('.txt'):
                    file_path = os.path.join(author_directory, file)
                    text_files.append((author, file_path))

    return text_files

def remove_diacritics(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', input_str)
        if not unicodedata.combining(c)
    )

def preprocess_text(text, remove_punctuation=True):
    text = text.lower()
    text = remove_diacritics(text)
    if remove_punctuation:
        text = re.sub(r'[^\w\s]', '', text)
    return text

def get_author_ngrams(directory, n):
    author_ngrams = defaultdict(list)
    text_files = get_texts_from_folder(directory)

    for author, file_path in text_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            text_content = preprocess_text(text_content)

            # Tokenize the text and generate n-grams
            tokens = nltk.word_tokenize(text_content)
            ngrams_list = list(ngrams(tokens, n))
            author_ngrams[author].extend(ngrams_list)

    return author_ngrams

def calculate_tfidf(author_ngrams):
    author_ngram_freq = defaultdict(Counter)
    document_count = Counter()
    total_authors = len(author_ngrams)

    # count the frequency of each n-gram for each author
    for author, ngrams in author_ngrams.items():
        author_ngram_freq[author] = Counter(ngrams)
        # Count the number of authors having each n-gram
        document_count.update(set(ngrams))

    # Calculate TF-IDF scores
    author_tfidf = defaultdict(dict)

    for author, ngram_freq in author_ngram_freq.items():
        total_ngrams = sum(ngram_freq.values())
        for ngram, count in ngram_freq.items():
            tf = count / total_ngrams
            idf = math.log(total_authors / (1 + document_count[ngram]))
            author_tfidf[author][ngram] = tf * idf

    return author_tfidf

def get_top_tfidf_ngrams(author_tfidf, top_n=10):
    top_ngrams_per_author = {}

    for author, ngram_scores in author_tfidf.items():
        sorted_ngrams = sorted(ngram_scores.items(), key=lambda x: x[1], reverse=True)
        top_ngrams_per_author[author] = sorted_ngrams[:top_n]

    return top_ngrams_per_author

def get_author_word_frequencies(directory):
    author_word_freq = defaultdict(Counter)
    text_files = get_texts_from_folder(directory)

    for author, file_path in text_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            text_content = preprocess_text(text_content)
            tokens = nltk.word_tokenize(text_content)
            author_word_freq[author].update(tokens)
    return author_word_freq

def get_author_word_lengths(directory):
    author_word_lengths = defaultdict(list)
    text_files = get_texts_from_folder(directory)

    for author, file_path in text_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            text_content = preprocess_text(text_content)
            tokens = nltk.word_tokenize(text_content)
            word_lengths = [len(word) for word in tokens]
            author_word_lengths[author].extend(word_lengths)
    return author_word_lengths

def get_author_sentence_lengths(directory):
    author_sentence_lengths = defaultdict(list)
    text_files = get_texts_from_folder(directory)

    for author, file_path in text_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            text_content = preprocess_text(text_content, remove_punctuation=False)
            sentences = nltk.sent_tokenize(text_content)
            for sentence in sentences:
                sentence = preprocess_text(sentence)
                tokens = nltk.word_tokenize(sentence)
                author_sentence_lengths[author].append(len(tokens))
    return author_sentence_lengths

def calculate_statistics(lengths):
    return {
        'mean': np.mean(lengths),
        'median': np.median(lengths),
        'std_dev': np.std(lengths),
        'min': np.min(lengths),
        'max': np.max(lengths)
    }

path = '/Users/tudor14/PycharmProjects/PhonostatisticsRo1/data acquisition/Carti copy'

author_bigrams = get_author_ngrams(path, 2)
author_trigrams = get_author_ngrams(path, 3)

bigram_tfidf = calculate_tfidf(author_bigrams)
trigram_tfidf = calculate_tfidf(author_trigrams)

top_bigrams_tfidf = get_top_tfidf_ngrams(bigram_tfidf, top_n=10)
top_trigrams_tfidf = get_top_tfidf_ngrams(trigram_tfidf, top_n=10)

author_word_freq = get_author_word_frequencies(path)
author_word_lengths = get_author_word_lengths(path)

author_sentence_lengths = get_author_sentence_lengths(path)

author_word_stats = {author: calculate_statistics(lengths) for author, lengths in author_word_lengths.items()}
author_sentence_stats = {author: calculate_statistics(lengths) for author, lengths in author_sentence_lengths.items()}

for author in author_word_freq:
    print(f"\nAuthor: {author}")
    print("Top TF-IDF Bigrams:")
    for bigram, score in top_bigrams_tfidf[author]:
        print(f"{bigram}: {score}")
    print("Top TF-IDF Trigrams:")
    for trigram, score in top_trigrams_tfidf[author]:
        print(f"{trigram}: {score}")
    print("Most Common Words:")
    for word, count in author_word_freq[author].most_common(10):
        print(f"{word}: {count}")
    print("Word Length Statistics:")
    for stat, value in author_word_stats[author].items():
        print(f"{stat.capitalize()}: {value}")
    print("Sentence Length Statistics:")
    for stat, value in author_sentence_stats[author].items():
        print(f"{stat.capitalize()}: {value}")


def plot_word_length_distribution(author_word_lengths):
    for author, lengths in author_word_lengths.items():
        plt.figure(figsize=(10, 6))
        sns.histplot(lengths, bins=range(1, 20), kde=True)
        plt.title(f'Word Length Distribution for {author}')
        plt.xlabel('Word Length')
        plt.ylabel('Frequency')
        plt.show()

def plot_sentence_length_distribution(author_sentence_lengths):
    for author, lengths in author_sentence_lengths.items():
        plt.figure(figsize=(10, 6))
        sns.histplot(lengths, bins=range(1, 100), kde=True)
        plt.title(f'Sentence Length Distribution for {author}')
        plt.xlabel('Sentence Length (Number of Words)')
        plt.ylabel('Frequency')
        plt.show()


def plot_word_frequencies(author_word_freq):
    for author, word_freq in author_word_freq.items():
        common_words = word_freq.most_common(20)
        words = [word for word, count in common_words]
        counts = [count for word, count in common_words]

        plt.figure(figsize=(12, 6))
        sns.barplot(x=counts, y=words)
        plt.title(f'Most Common Words for {author}')
        plt.xlabel('Frequency')
        plt.ylabel('Words')
        plt.show()

# Plotting
# plot_word_length_distribution(author_word_lengths)
# plot_sentence_length_distribution(author_sentence_lengths)
# plot_word_frequencies(author_word_freq)

