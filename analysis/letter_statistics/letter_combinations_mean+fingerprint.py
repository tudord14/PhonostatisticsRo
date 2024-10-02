import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk
from tkinter.filedialog import askdirectory


"""

This function does the following:
    -> Once the user runs it a folder containing more .csv files can be used
    -> The .csv files should be the ones obtained by running "letter_combinations_extraction.py"
    -> The files should have the following structure: "..._Combinations_WaitingTimes.csv"
    -> This function should take the csvs and create for each one two more .csv files :)
        -> "..._global_mean_percentages_adjusted.csv"
            -> will contain a column with all the letter combinations
            -> for every combination we take every value that the column has and calculate
               the Mean for each comb
        -> "_fingerprint_matrix_adjusted.csv"
            -> this file will contain a 26x26 matrix with all the possible letter combinations
            -> the matrix has for rows and columns the alphabet, so that we can create every possible comb
            -> we plug each value from "..._global_mean_percentages_adjusted.csv" in this matrix in its
               correct place
    
    -> At the end we can plot the fingerprint matrix using the "show_fingerprint_matrix" function
    
"""


def calculate_global_normalized_mean_combinations_for_folder():
    Tk().withdraw()

    print("Please select the folder containing the CSV files.")
    folder_path = askdirectory(title="Select a folder containing CSV files")

    if folder_path:
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

        for file_path in csv_files:
            print(f"Processing file: {file_path}")

            data = pd.read_csv(file_path)
            data = data.fillna(0)
            data = data.apply(pd.to_numeric, errors='coerce').fillna(0)
            grand_total = data.sum().sum()

            if grand_total == 0:
                print(f"File {file_path} contains only zeros")
                continue

            normalized_data = (data / grand_total) * 100
            mean_percentages = normalized_data.mean()
            total_mean = mean_percentages.sum()
            adjusted_mean_percentages = (mean_percentages / total_mean) * 100

            output_path = file_path.replace(".csv", "_global_mean_percentages_adjusted.csv")
            adjusted_mean_percentages.to_csv(output_path, header=['Mean Percentage'], index_label='Combination')
            print(f"Global mean percentages saved to: {output_path}")

            fingerprint_matrix = np.zeros((26, 26))
            letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]

            for combination, mean_value in adjusted_mean_percentages.items():
                if len(combination) == 2:
                    first_letter, second_letter = combination[0], combination[1]
                    if first_letter in letters and second_letter in letters:
                        row = letters.index(first_letter)
                        col = letters.index(second_letter)
                        fingerprint_matrix[row, col] = mean_value

            fingerprint_df = pd.DataFrame(fingerprint_matrix, index=letters, columns=letters)

            fingerprint_output_path = file_path.replace(".csv", "_fingerprint_matrix_adjusted.csv")
            fingerprint_df.to_csv(fingerprint_output_path)
            print(f"Fingerprint saved to: {fingerprint_output_path}")

            #show_fingerprint_matrix(fingerprint_df)
    else:
        print("No folder selected!")

def show_fingerprint_matrix(fingerprint_df):
    plt.figure(figsize=(10, 8))
    sns.heatmap(fingerprint_df, annot=False, cmap="viridis", cbar_kws={'label': 'Mean Percentage'})
    plt.title("Text Fingerprint Matrix", fontsize=16)
    plt.xlabel("Second Letter")
    plt.ylabel("First Letter")
    plt.show()


calculate_global_normalized_mean_combinations_for_folder()
