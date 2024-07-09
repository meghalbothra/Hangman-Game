import tkinter as tk
from tkinter import messagebox
import random

# Dictionary of words with their corresponding hints
word_dict = {
    "python": "A popular programming language.",
    "hangman": "The name of this game.",
    "programming": "The process of writing computer programs.",
    "tkinter": "A Python library for creating graphical user interfaces.",
    "interface": "A shared boundary across which information is exchanged."
}

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.word, self.hint = random.choice(list(word_dict.items()))
        self.guessed_word = ["_"] * len(self.word)
        self.attempts_left = 6
        self.guessed_letters = set()

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.word_label = tk.Label(self.root, text=" ".join(self.guessed_word), font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        self.hint_label = tk.Label(self.root, text=f"Hint: {self.hint}", font=("Helvetica", 14))
        self.hint_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.guess_letter)

        self.guess_button = tk.Button(self.root, text="Guess", command=self.guess_letter)
        self.guess_button.pack(pady=10)

        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.message_label.pack(pady=10)

        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.attempts_left}", font=("Helvetica", 14))
        self.attempts_label.pack(pady=10)

        self.draw_hangman()

    def guess_letter(self, event=None):
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not letter.isalpha() or len(letter) != 1:
            self.message_label.config(text="Please enter a single alphabetic character.")
            return

        if letter in self.guessed_letters:
            self.message_label.config(text="You already guessed that letter.")
            return

        self.guessed_letters.add(letter)

        if letter in self.word:
            for idx, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[idx] = letter
            self.word_label.config(text=" ".join(self.guessed_word))
            self.message_label.config(text="Good guess!")
        else:
            self.attempts_left -= 1
            self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
            self.message_label.config(text="Wrong guess.")
            self.draw_hangman()

        if "_" not in self.guessed_word:
            self.end_game("Congratulations! You guessed the word!")
        elif self.attempts_left == 0:
            self.end_game(f"Game Over! The word was: {self.word}")

    def draw_hangman(self):
        self.canvas.delete("all")
        self.canvas.create_line(100, 300, 300, 300)
        self.canvas.create_line(200, 300, 200, 50)
        self.canvas.create_line(200, 50, 250, 50)
        self.canvas.create_line(250, 50, 250, 100)

        if self.attempts_left <= 5:
            self.canvas.create_oval(230, 100, 270, 140)  # Head
        if self.attempts_left <= 4:
            self.canvas.create_line(250, 140, 250, 220)  # Body
        if self.attempts_left <= 3:
            self.canvas.create_line(250, 160, 220, 190)  # Left Arm
        if self.attempts_left <= 2:
            self.canvas.create_line(250, 160, 280, 190)  # Right Arm
        if self.attempts_left <= 1:
            self.canvas.create_line(250, 220, 220, 270)  # Left Leg
        if self.attempts_left == 0:
            self.canvas.create_line(250, 220, 280, 270)  # Right Leg

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
