import tkinter as tk
from tkinter import messagebox
import random
import time

MAX_ATTEMPTS = 6

# Function to check the guess against the secret word
def check_guess(event=None):
    global secret_word, attempts_left

    guess = entry.get().upper()
    if len(guess) != len(secret_word):
        messagebox.showerror("Error", "Guess must be {} letters long.".format(len(secret_word)))
        return
    
    feedback_frame = tk.Frame(history_frame)
    feedback_frame.pack(fill=tk.X)

    correct_guess = True

    for i, char in enumerate(guess):
        label = tk.Label(feedback_frame, text=char, width=2, height=1, font=("Helvetica", 18))
        label.pack(side=tk.LEFT, padx=1, pady=1)

        if char == secret_word[i]:
            label.config(bg="green", fg="white")
        elif char in secret_word:
            label.config(bg="yellow", fg="black")
            correct_guess = False
        else:
            label.config(bg="grey", fg="white")
            correct_guess = False
    
    entry.delete(0, tk.END)
    
    if correct_guess:
        flip_board(secret_word)  # Animate the reveal of the correct word
        entry.config(state=tk.DISABLED)
        messagebox.showinfo("Congratulations!", "You guessed the word!")
    else:
        attempts_left -= 1
        update_attempts_display()

        if attempts_left == 0:
            messagebox.showinfo("Game Over", f"You ran out of attempts!\nThe word was: {secret_word}")
            entry.config(state=tk.DISABLED)
            reset_game()

# Function to reset the game
def reset_game(event=None):
    global secret_word, attempts_left

    # Choose a new random word
    secret_word = random.choice(word_list).strip().upper()
    
    # Update the stored secret_word.txt file (optional)
    with open("secret_word.txt", "w") as file:
        file.write(secret_word)
    
    # Reset attempts count
    attempts_left = MAX_ATTEMPTS
    update_attempts_display()
    
    # Enable entry for new guesses
    entry.config(state=tk.NORMAL)
    
    # Clear history_frame
    for widget in history_frame.winfo_children():
        widget.destroy()

# Function to update attempts display
def update_attempts_display():
    for child in attempts_frame.winfo_children():
        child.destroy()
    
    remaining_attempts = "Attempts Remaining: " + " ".join(["◻️"] * attempts_left)
    attempts_label = tk.Label(attempts_frame, text=remaining_attempts, font=("Helvetica", 14))
    attempts_label.pack(pady=10)

# Function to animate the reveal of the correct word with flipboard effect
def flip_board(word):
    # Clear history_frame
    for widget in history_frame.winfo_children():
        widget.destroy()

    flip_labels = []
    for char in word:
        label = tk.Label(history_frame, text="*", width=2, height=1, font=("Helvetica", 18), bg="white", fg="black")
        label.pack(side=tk.LEFT, padx=1, pady=1)
        flip_labels.append(label)

    root.update()

    for label in flip_labels:
        label.config(text=label["text"], bg="green", fg="white")
        root.update()
        time.sleep(0.2)

# Load words from file
with open("words.txt", "r") as file:
    word_list = file.readlines()

# Choose initial secret word
secret_word = random.choice(word_list).strip().upper()
with open("secret_word.txt", "w") as file:
    file.write(secret_word)

# Set up the main window
root = tk.Tk()
root.title("WORDLE")
root.geometry("400x400")

# Heading label
heading_label = tk.Label(root, text="WORDLE", font=("Helvetica", 24, "bold"))
heading_label.pack(pady=10)

# Entry field for guesses
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, font=("Helvetica", 18), width=10)
entry.pack(side=tk.LEFT, padx=5)

guess_button = tk.Button(entry_frame, text="Guess", command=check_guess)
guess_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(entry_frame, text="Reset", command=reset_game)
reset_button.pack(side=tk.LEFT, padx=5)

# Frame to display guess history
history_frame = tk.Frame(root)
history_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=50)

# Frame to display attempts remaining
attempts_frame = tk.Frame(root)
attempts_frame.pack(fill=tk.X, pady=30)

# Display initial attempts remaining
attempts_left = MAX_ATTEMPTS
update_attempts_display()

# Footer label
footer_label = tk.Label(root, text="Created by Ayush Singh (AD)", font=("Helvetica", 10))
footer_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)

# Bind Enter key to check_guess function
root.bind('<Return>', check_guess)

# Bind Esc key to reset_game function
root.bind('<Escape>', reset_game)

# Start the Tkinter event loop
root.mainloop()
