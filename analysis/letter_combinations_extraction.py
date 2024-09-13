import pandas as pd
import unicodedata
import os
from tkinter import Tk, filedialog, messagebox


"""

 Dictionary that holds all the letters of the alphabet

"""

dictionar = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
    'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
    'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15,
    'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20,
    'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26
}


"""

 Function that removes diacritics from a text and returns the new text

"""

def remove_diacritics(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', input_str)
        if not unicodedata.combining(c)
    )


"""

 Function that takes in a file and returns a .csv with letter combinations
   -> As output we get a dataframe that has a lot of columns that represent
      letter combinations like: "ad", "bg", ...
   -> Each row represents the time it took to find the specific letter comb

"""

def process_text_file(file_path, delta=1):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Text without diacritics
    cleaned_text = remove_diacritics(text_content.lower())

    # Transform text into numbers
    transf = [dictionar[ch] for ch in cleaned_text if ch in dictionar]

    # Filter the text, save only the characters that are in the dictionary
    # For example don't save: , . ; ? / ! ..., only a b c d ...
    litereTrue = [ch for ch in cleaned_text if ch in dictionar]

    # A map of the letter combinations and the waiting time that it took to form
    # that specific combination
    combinations_map_simplified = simplified_timpi_with_combinations(transf, litereTrue, delta)

    # Transform into a dataframe for easier extraction
    combinations_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in combinations_map_simplified.items()]))

    return combinations_df


"""

 Waiting time calculation:
   -> this function calculates waiting times for each combination
      and adds the waiting time to the corresponding letter combination column
      from the dataframe
   -> so that each waiting time is correctly added to the good column

"""

def simplified_timpi_with_combinations(magnit, litereTrue, delta):
    timpi_astep_map = {}
    lungime2 = len(magnit)

    for i in range(lungime2 - 1):
        for j in range(i + 1, lungime2):
            if magnit[j] >= (magnit[i] + delta):
                combinatie = litereTrue[i] + litereTrue[j]

                if combinatie not in timpi_astep_map:
                    timpi_astep_map[combinatie] = []
                timpi_astep_map[combinatie].append(j - i)
                break

    return timpi_astep_map


"""

 Function that simplifies the analysis part:
   -> It gives the user the possibility to input a folder containing .txt files
      so that the analysis can be done on more texts at once

"""

def select_and_process_multiple_folders():
    Tk().withdraw()

    folders = []
    while True:
        folder_path = filedialog.askdirectory(title="Select a folder containing text files")
        if folder_path:
            folders.append(folder_path)
        else:
            break
        if not messagebox.askyesno("Select More?", "Do you want to select another folder?"):
            break

    for directory_path in folders:
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                combinations_df = process_text_file(file_path)

                output_csv_path = os.path.join(directory_path,
                                               f"{os.path.splitext(filename)[0]}_Combinations_WaitingTimes_delta1.csv")
                combinations_df.to_csv(output_csv_path, index=False)

                print(f"Processed {filename} and saved to {output_csv_path}")

if __name__ == "__main__":
    select_and_process_multiple_folders()
