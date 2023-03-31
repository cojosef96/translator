import os
import random
import tkinter as tk
from gtts import gTTS
from playsound import playsound
from tkinter import messagebox


class AudioPlayerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Audio Player")
        self.window.geometry("400x200")

        self.talking_sentence_label = tk.Label(self.window, text="Not showing")
        self.talking_sentence_label.pack()

        self.translated_sentence_label = tk.Label(self.window, text="Not showing")
        self.translated_sentence_label.pack()

        self.language_label = tk.Label(self.window, text="Language: ")
        self.language_label.pack()

        self.hear_button = tk.Button(self.window, text="Hear", command=self.play_audio)
        self.hear_button.pack()

        self.reveal_button = tk.Button(self.window, text="Reveal", command=self.reveal_sentences)
        self.reveal_button.pack()

        self.audio_files = []
        for filename in os.listdir("mp3_audio"):
            if filename.endswith(".mp3"):
                self.audio_files.append(os.path.join("mp3_audio", filename))

    def run(self):
        self.window.mainloop()
    def play_audio(self):
        if not self.audio_files:
            messagebox.showinfo("No Audio Files", "No audio files found in mp3_audio directory.")
            return
        if self.current_audio_file:
            playsound(self.current_audio_file)

    def reveal_sentences(self):
        if not self.audio_files:
            messagebox.showinfo("No Audio Files", "No audio files found in mp3_audio directory.")
            return
        if self.current_audio_file:
            filename = os.path.basename(self.current_audio_file)
            sentence, language = os.path.splitext(filename)[0].split("_")
            translated_sentence = self.translate_sentence(sentence, language)
            self.talking_sentence.set(sentence)
            self.translated_sentence.set(translated_sentence)
            self.language_choice.set(language)

    def next_audio(self):
        if not self.audio_files:
            messagebox.showinfo("No Audio Files", "No audio files found in mp3_audio directory.")
            return
        self.current_audio_file = random.choice(self.audio_files)
        self.play_audio()
        self.reveal_sentences()


if __name__ == "__main__":
    gui = AudioPlayerGUI()
    gui.run()
