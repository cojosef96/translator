
import csv
import tkinter as tk
from tkinter import ttk
from googletrans import LANGUAGES
from enum import Enum
from gtts import gTTS
from translators import TranslatorType, Translator
from autocomplete_combo_box import AutocompleteLanguageCombobox
import os
import subprocess
from tkinter import messagebox
import datetime


root = tk.Tk()
root.geometry('700x600')
root.title('Translation App')


class TranslationApp:
    def __init__(self, master):
        self.master = master
        self.language_codes = {v: k for k, v in LANGUAGES.items()}

        # Create UI elements
        self.create_input_section()
        self.create_language_sections()
        self.create_service_section()
        self.create_translation_button()
        self.create_output_section()
        self.create_text_to_speech_button()
        self.create_save_audio_button()

    def create_input_section(self):
        input_label = tk.Label(self.master, text='Input Text:')
        input_label.pack()

        self.input_textbox = tk.Text(self.master, height=5, width=50)
        self.input_textbox.pack()

    def create_language_sections(self):
        self.create_from_lang_section()
        self.create_to_lang_section()

    def create_from_lang_section(self):
        from_lang_label = tk.Label(self.master, text='Translate from:')
        from_lang_label.pack()

        self.from_lang_choice = AutocompleteLanguageCombobox(self.master)
        self.from_lang_choice.set_completion_list(self.language_codes)
        self.from_lang_choice.current(list(self.language_codes.keys()).index('english'))
        self.from_lang_choice.pack()

    def create_to_lang_section(self):
        lang_label = tk.Label(self.master, text='Translate to:')
        lang_label.pack()

        self.lang_choice = AutocompleteLanguageCombobox(self.master)
        self.lang_choice.set_completion_list(self.language_codes)
        self.lang_choice.current(list(self.language_codes.keys()).index('french'))
        self.lang_choice.pack()

    def create_service_section(self):
        service_label = tk.Label(self.master, text='Translation Service:')
        service_label.pack()

        self.translator_choice = tk.StringVar()
        self.translator_choice.set(TranslatorType.GOOGLE.name)

        self.create_translator_buttons()

    def create_translator_buttons(self):
        translator_frame = tk.Frame(self.master)
        translator_frame.pack()
        google_radio = tk.Radiobutton(translator_frame, text=TranslatorType.GOOGLE.name.capitalize(),
                                      variable=self.translator_choice, value=TranslatorType.GOOGLE.name)
        reverso_radio = tk.Radiobutton(translator_frame, text=TranslatorType.REVERSO.name.capitalize(),
                                       variable=self.translator_choice, value=TranslatorType.REVERSO.name)
        google_radio.pack(side=tk.LEFT)
        reverso_radio.pack(side=tk.LEFT)

    def create_translation_button(self):
        translate_button = tk.Button(self.master, text='Translate', command=self.translate, height=2, width=15)
        translate_button.pack(pady=10)

        reverse_lang_button = tk.Button(self.master, text='Reverse Language', command=self.reverse_language, height=2,
                                        width=15)
        reverse_lang_button.pack(pady=10)

    def create_output_section(self):
        output_label = tk.Label(self.master, text='Translation:')
        output_label.pack()

        self.output_text = tk.Text(self.master, height=5, width=50)
        self.output_text.pack()

    def reverse_language(self):
        from_lang = self.from_lang_choice.get()
        to_lang = self.lang_choice.get()

        self.from_lang_choice.set(to_lang)
        self.lang_choice.set(from_lang)

    def reverse_languages(self):
        # Get the current selected languages
        current_from_lang = self.from_lang_choice.get()
        current_to_lang = self.lang_choice.get()

        # Reverse the languages
        self.from_lang_choice.set(current_to_lang)
        self.lang_choice.set(current_from_lang)

    def create_text_to_speech_button(self):
        tts_button = tk.Button(self.master, text='Text-to-Speech', command=self.text_to_speech, height=2, width=15)
        tts_button.pack(pady=10)

    def create_save_audio_button(self):
        save_audio_button = tk.Button(self.master, text='Save Audio', command=self.save_audio, height=2, width=15)
        save_audio_button.pack(pady=10)

    def text_to_speech(self):
        input_text = self.output_text.get("1.0", "end-1c")
        language = self.language_codes[self.lang_choice.get()]

        tts = gTTS(text=input_text, lang=language, slow=False)
        tts.save("output.mp3")

        # Play audio
        subprocess.call(['mplayer', 'output.mp3'])

        # Show success message
        self.show_message("Text to speech conversion successful!")

    def save_audio(self):
        input_text = self.output_text.get("1.0", tk.END).strip()
        language = self.lang_choice.get()
        filename = f"{input_text}_{language}.mp3"
        filepath = os.path.join("mp3_audio", filename)
        # Check if mp3_audio directory exists, create it if it doesn't
        if not os.path.exists("mp3_audio"):
            os.makedirs("mp3_audio")
        tts = gTTS(text=input_text, lang=self.language_codes[language])
        tts.save(filepath)
        messagebox.showinfo("Audio Saved", f"Audio file saved as {filename} in mp3_audio directory.")


    def show_message(self, message):
        message_label = tk.Label(self.master, text=message)
        message_label.pack()

    def translate(self):
        input_text = self.input_textbox.get("1.0", tk.END).strip()
        from_lang = self.from_lang_choice.get()
        to_lang = self.lang_choice.get()

        translator_type = self.translator_choice.get()
        translator = Translator(translator_type)
        translated = translator.translate(input_text, self.language_codes[from_lang],self.language_codes[to_lang])
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, translated)
        now = datetime.datetime.now()

        with open('translations.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Input Text', 'Translation', 'From Language', 'To Language', 'Framework', 'date', 'time'])
            writer.writerow([input_text, translated, from_lang, to_lang, translator_type, now.strftime('%d-%m-%Y'), now.strftime('%H:%M:%S')])



app = TranslationApp(root)

root.mainloop()
