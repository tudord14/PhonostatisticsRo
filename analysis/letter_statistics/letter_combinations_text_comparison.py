import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from sklearn.metrics.pairwise import cosine_similarity


"""

This function works by using the fingerprint obtained from "letter_combinations_mean+fingerprint.py"
and comparing it to another fingerprint of another text.
By running this we can obtain a basic comparison between two texts.
-> Because the fingerprints are in the structure of a matrix we make use of the 
   cosine similarity to compare the texts
-> The fingerprint matrix was created so that this comparison can be made like this

"""


def compare_two_texts():
    Tk().withdraw()

    print("Select the fingerprint matrix for the first text")
    file_path_1 = askopenfilename(title="Select the first fingerprint matrix CSV file", filetypes=[("CSV files", "*.csv")])

    if not file_path_1:
        print("No file selected for the first text!")
        return

    print("Select the fingerprint matrix for the second text")
    file_path_2 = askopenfilename(title="Select the second fingerprint matrix CSV file", filetypes=[("CSV files", "*.csv")])

    if not file_path_2:
        print("No file selected for the second text!")
        return

    fingerprint_1 = pd.read_csv(file_path_1, index_col=0).values
    fingerprint_2 = pd.read_csv(file_path_2, index_col=0).values

    vector_1 = fingerprint_1.flatten()
    vector_2 = fingerprint_2.flatten()

    cosine_sim = cosine_similarity([vector_1], [vector_2])[0][0]

    print(f"Cosine Similarity: {cosine_sim:.4f}")


compare_two_texts()
