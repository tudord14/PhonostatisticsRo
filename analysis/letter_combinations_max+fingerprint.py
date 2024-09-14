import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog, messagebox

"""

This function does the following:
    -> Once the user runs it a folder containing more .csv files can be used
    -> The .csv files should be the ones obtained by running "letter_combinations_extraction.py"
    -> The files should have the following structure: "..._Combinations_WaitingTimes.csv"
    -> This function should take the csvs and create for each one two more .csv files :)
        -> "..._global_max_percentages_adjusted.csv"
            -> will contain a column with all the letter combinations
            -> for every combination we find the maximum waiting time value for each comb
            -> I like to call it the 'impact parameter'
        -> "_fingerprint_matrix_adjusted.csv"
            -> this file will contain a 26x26 matrix with all the possible letter combinations
            -> the matrix has for rows and columns the alphabet, so that we can create every possible comb
            -> we plug each value from "..._global_max_percentages_adjusted.csv" in this matrix in its
               correct place
    
        -> A choice can be made by the user at line 73, so that one can choose 
        how many combinations he wants to take into account in the analysis
        -> The comment there takes the first 100 most important combinations!

    -> At the end we can plot the fingerprint matrix using the "show_fingerprint_matrix" function

"""

def calculate_global_normalized_max_combinations_for_multiple_folders():
    Tk().withdraw()

    folders = []
    while True:
        print("Please select a folder containing the CSV files.")
        folder_path = filedialog.askdirectory(title="Select a folder containing CSV files")

        if folder_path:
            folders.append(folder_path)
        else:
            break

        if not messagebox.askyesno("Select More?", "Do you want to select another folder?"):
            break

    if folders:
        for folder_path in folders:
            csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

            for file_path in csv_files:
                print(f"Processing file: {file_path}")

                data = pd.read_csv(file_path)

                data = data.fillna(0)
                data = data.apply(pd.to_numeric, errors='coerce').fillna(0)

                grand_total = data.sum().sum()

                if grand_total == 0:
                    print(f"File {file_path} contains only zero values or no valid data. Skipping...")
                    continue

                normalized_data = (data / grand_total) * 100
                max_percentages = normalized_data.max()
                sorted_max_percentages = max_percentages.sort_values(ascending=False)

                #######################
                #filtered_max_percentages = sorted_max_percentages.iloc[100:]
                ######################

                filtered_max_percentages = sorted_max_percentages

                output_path = file_path.replace(".csv", "_global_max_percentages_adjusted.csv")
                filtered_max_percentages.to_csv(output_path, header=['Impact Percentage'], index_label='Combination')
                print(f"Global max percentages saved to: {output_path}")

                fingerprint_matrix = np.zeros((26, 26))
                letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]

                for combination, impact_value in filtered_max_percentages.items():
                    if len(combination) == 2:
                        first_letter, second_letter = combination[0], combination[1]
                        if first_letter in letters and second_letter in letters:
                            row = letters.index(first_letter)
                            col = letters.index(second_letter)
                            fingerprint_matrix[row, col] = impact_value

                fingerprint_df = pd.DataFrame(fingerprint_matrix, index=letters, columns=letters)

                fingerprint_output_path = file_path.replace(".csv", "_fingerprint_matrix_adjusted.csv")
                fingerprint_df.to_csv(fingerprint_output_path)
                print(f"Fingerprint saved to: {fingerprint_output_path}")

                # Uncomment the following line to display the heatmap
                # show_fingerprint_matrix(fingerprint_df)
    else:
        print("No folders selected!")

def show_fingerprint_matrix(fingerprint_df):
    plt.figure(figsize=(10, 8))
    sns.heatmap(fingerprint_df, annot=False, cmap="viridis", cbar_kws={'label': 'Impact Percentage'})
    plt.title("Text Fingerprint Matrix", fontsize=16)
    plt.xlabel("Second Letter")
    plt.ylabel("First Letter")
    plt.show()

calculate_global_normalized_max_combinations_for_multiple_folders()
