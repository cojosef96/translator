import csv
import random
import tkinter as tk

root = tk.Tk()
root.geometry('500x300')
root.title('Random Translation')

translations = []

with open('translations.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        translations.append(row)

def reveal_translation():
    global current_translation
    current_input_text = current_translation['Input Text']
    input_text_label.config(text='Input Text: ' + current_input_text)
    translation_label.config(text='Translation: ' + current_translation['Translation'])
    from_lang_label.config(text='From Language: ' + current_translation['From Language'])
    to_lang_label.config(text='To Language: ' + current_translation['To Language'])
    reveal_button.config(state='disabled')

def next_translation():
    global current_translation
    current_translation = random.choice(translations)
    input_text_label.config(text='')
    translation_label.config(text='Translation: ' + current_translation['Translation'])
    from_lang_label.config(text='From Language: ' + current_translation['From Language'])
    to_lang_label.config(text='To Language: ' + current_translation['To Language'])
    reveal_button.config(state='normal')

current_translation = random.choice(translations)

input_text_label = tk.Label(root, text='')
input_text_label.pack(pady=10)

translation_label = tk.Label(root, text='Translation: ' + current_translation['Translation'])
translation_label.pack(pady=10)

from_lang_label = tk.Label(root, text='From Language: ' + current_translation['From Language'])
from_lang_label.pack(pady=10)

to_lang_label = tk.Label(root, text='To Language: ' + current_translation['To Language'])
to_lang_label.pack(pady=10)

reveal_button = tk.Button(root, text='Reveal Translation', command=reveal_translation, height=2, width=15)
reveal_button.pack(pady=10)

next_button = tk.Button(root, text='Next Translation', command=next_translation, height=2, width=15)
next_button.pack(pady=10)

root.mainloop()
