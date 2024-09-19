# PhonostatisticsRo

The goal of this project is to analyze different languages using statistical models, aiming to uncover properties that offer deeper insights into their structure. Initially developed to study the Romanian language, all functions are designed to be adaptable for any language.

At the moment, the project consists of **three folders**, though only **two** contain code so far (*I hope this will change soon!*). When looking at the contents of each directory, one might ask, *"How does it all fit together?"* That's a completely reasonable question, as the components were developed over several weeks. Instead of being one unified codebase, each folder corresponds to a small but important part of the overall project.

In this description, I'll try my best to outline how these pieces come together, and how anyone interested can unravel and maybe even build upon this code for further research. Stay tuned for more updates as the project continues to evolve!

**(statistical models used and their properties...to be completed!)**

## **Analysis Directory**
*(The project uses **folders** (corresponding to an author) that hold multiple **.txt files** representing texts written by that author.)*

We start by assuming that the interested user has already obtained their database and is ready to study their texts!


**The first step** should be running both of the **.py** files that have the word **extraction** in them.
- **`waiting_times_extraction.py`** takes as input a folder and outputs one **.csv** file containing the waiting times for each text from that folder.

- **`letter_combination_extraction.py`** takes as input a folder and outputs a **.csv** file containing multiple columns representing different letter combinations found in the text. The row values represent the waiting times when that combination has been found throughout the text.

**The second step** is obtaining the **author/text fingerprint matrix** so that we can later compare it to another. To do this we can use one of the two following programs:

- **`letter_combinations_max+fingerprint.py`**
  
- **`letter_combinations_mean+fingerprint.py`**

**The third step** is actually making comparisons between already obtained **fingerprint matrix** of different texts/authors by using the function:
- **`letter_combinations_text_comparison`**


## **Data Acquisition Directory**
*(These functions should work if the author can be found on **Project Gutenberg**)*

Acquiring and curating data can be a **time-consuming** task, especially when large datasets are needed. To help with this, here are some functions that will make data acquisition easier for the user:

- **`author_texts_extraction_epub_to_txt.py`** takes in an author's name and outputs a folder named after the author. This folder contains **.epub** and **.txt** files corresponding to texts written by that author.

- **`author_directory_cleanup.py`** cleans the folder created by the function above. It deletes the **.epub** files and ensures that the **.txt** files contain only the text of interest. This function removes Project Gutenberg's extra content and any other non-related text.








