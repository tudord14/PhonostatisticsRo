# PhonostatisticsRo

The goal of this project is to analyze different languages using statistical models, aiming to uncover properties that offer deeper insights into their structure. Initially developed to study the Romanian language, all functions are designed to be adaptable for any language.

At the moment, the project consists of **three folders**, though only **two** contain code so far (*I hope this will change soon!*). When looking at the contents of each directory, one might ask, *"How does it all fit together?"* That's a completely reasonable question, as the components were developed over several weeks. Instead of being one unified codebase, each folder corresponds to a small but important part of the overall project.

In this description, I'll try my best to outline how these pieces come together, and how anyone interested can unravel and maybe even build upon this code for further research. Stay tuned for more updates as the project continues to evolve!

**(statistical models used and their properties...to be completed!)**

## **Analysis Directory** ## 
 *(The project uses **folders**(corresponding to an author) that hold multiple **.txt files** that represent texts written by that author.)*
 
We start by assuming that the interested user has already obtained his database and is ready to study his texts!
**The first step** should be running both of the **.py** files that have the word **extraction** in them. 
**->** *"waiting_times_extraction.py"* takes as input a folder and outputs one 
       **.csv** file containing the waiting times for each text from that folder.
**->** *"letter_combination_extraction.py"* takes as input a folder and outputs     
       **.csv** file containing the multiple columns that represent different letter 
       combinations found in the text, and for the row values the waiting times when 
       when that combination has been found throughout the text







