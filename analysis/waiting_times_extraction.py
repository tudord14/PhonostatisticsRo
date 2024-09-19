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

 Function that takes in a file and returns a .csv with waiting times
    -> the .csv has one column with all the waiting times found 
    -> each row is a waiting time value
    
"""


def calculate_waiting_times(file_path, delta=15):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    cleaned_text = remove_diacritics(text_content.lower())

    transf = [dictionar[ch] for ch in cleaned_text if ch in dictionar]
    litereTrue = [ch for ch in cleaned_text if ch in dictionar]

    waiting_times = get_waiting_times(transf, litereTrue, delta)

    waiting_times_df = pd.DataFrame({'WaitingTimes': waiting_times})
    return waiting_times_df


"""

 Waiting time calculation:
   -> this function calculates waiting times
   -> it returns a list of waiting times

"""

def get_waiting_times(magnit, litereTrue, delta):
    waiting_times = []
    lungime2 = len(magnit)

    for i in range(lungime2 - 1):
        for j in range(i + 1, lungime2):
            if magnit[j] >= (magnit[i] + delta):
                waiting_times.append(j - i)
                break

    return waiting_times


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
                waiting_times_df = calculate_waiting_times(file_path)

                output_csv_path = os.path.join(directory_path,
                                               f"{os.path.splitext(filename)[0]}_WaitingTimes.csv")
                waiting_times_df.to_csv(output_csv_path, index=False)

                print(f"Processed {filename} and saved waiting times to {output_csv_path}")

if __name__ == "__main__":
    select_and_process_multiple_folders()
