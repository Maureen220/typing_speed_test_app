from tkinter import *
from word_list import word_list
import random

# ---------------------------- CONSTANTS ------------------------------- #
BLACK = "#000000"
WHITE = "#ffffff"
RED = "#ff0000"
FONT_NAME = "Courier"
ENTRIES = []
INCORRECT_WORDS = []
TIMER_RUNNING = False
TIME_ELAPSED = 60
IS_PLAYING = True


# ---------------------------- TRACKING ENTRY ------------------------------- #
def update_entry(user_input, word_label, entry_widget):
    global TIME_ELAPSED

    # Choose a word that has not been used yet
    unused_words = set(word_list) - set(ENTRIES)
    new_word = random.choice(list(unused_words))

    if TIME_ELAPSED > 0:
        word_label.config(text=new_word, font=(FONT_NAME, 50, "bold"), bg=BLACK, fg=WHITE)
        word_label.place(x=275, y=125)
        entry_widget.delete(0, END)

        # Need to remove space in list
        entry = user_input.strip()

        if entry in word_list:
            ENTRIES.append(entry)
        else:
            if entry != "":
                INCORRECT_WORDS.append(entry)
    else:
        # Update word label
        word_label.config(text="GAME OVER")
        word_to_type_label.place(x=200, y=125)

        # Update entry widget
        entry_widget.delete(0, END)
        entry_widget.insert(0, "Click 'Results'")


# # ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer(*args):
    global TIMER_RUNNING
    if not TIMER_RUNNING:
        TIMER_RUNNING = True
        update_timer()


def update_timer():
    global TIME_ELAPSED
    if TIMER_RUNNING:
        if TIME_ELAPSED > 9:
            timer_label.config(text=f"00:{TIME_ELAPSED}")
            window.after(1000, update_timer)  # Update every 1000 milliseconds (1 second)
            TIME_ELAPSED -= 1
        elif TIME_ELAPSED > 0:
            timer_label.config(text=f"00:0{TIME_ELAPSED}")
            window.after(1000, update_timer)
            TIME_ELAPSED -= 1
        else:
            timer_label.config(text=f"00:00 TIME'S UP!", fg=RED)
            timer_label.place(x=200, y=70)


# ---------------------------- RESET GAME ------------------------------- #
def reset_game():
    global ENTRIES, INCORRECT_WORDS, TIMER_RUNNING, TIME_ELAPSED

    # Clear previous game data
    ENTRIES = []
    INCORRECT_WORDS = []
    TIMER_RUNNING = False
    TIME_ELAPSED = 60

    # Reset labels
    timer_label.config(text="01:00", fg=WHITE)
    word_to_type_label.config(text="Press 'Space' to start.", font=(FONT_NAME, 30, "bold"), bg=BLACK, fg=WHITE)
    word_to_type_label.place(x=150, y=125)

    # Clear entry
    typing_entry.delete(0, END)

    # Reset timer label position
    timer_label.place(x=330, y=70)

    # Destroy result labels if they exist
    for widget in window.winfo_children():
        if isinstance(widget, Label) and "results" in widget.cget("text").lower():
            widget.destroy()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Speed Test")
window.config(padx=100, pady=50, bg=BLACK)

# Set the position of the window on the screen. Set for 1920 x 1080 monitor
window_x = 400
window_y = 50
window.geometry(f"+{window_x}+{window_y}")

# Canvas
canvas = Canvas(width=800, height=824, bg=BLACK, highlightthickness=0)
typewriter_img = PhotoImage(file="images/typewriter_medium.png")
canvas.create_image(380, 475, image=typewriter_img)
canvas.grid(column=1, row=1)

# Labels
instructions = Label(text="You have 60 seconds to type as many words as possible. Use 'SPACE BAR' for next word. "
                          "Start typing to start timer.",
                     font=(FONT_NAME, 18, "bold"), bg=BLACK, fg=WHITE, wraplength=900)
instructions.place(x=30, y=0)

timer_label = Label(text="01:00", font=(FONT_NAME, 35, "bold"), bg=BLACK, fg=WHITE)
timer_label.place(x=330, y=70)

word_to_type_label = Label(text="Press 'Space' to start.", font=(FONT_NAME, 30, "bold"), bg=BLACK, fg=WHITE)
word_to_type_label.place(x=150, y=125)

# Entries
typing_entry = Entry(width=80)
typing_entry.place(x=150, y=215)
typing_entry.focus()
typing_entry.bind("<space>", (lambda event: update_entry(typing_entry.get(), word_to_type_label, typing_entry)))
typing_entry.bind("<Key>", start_timer)

# Buttons
reset_button = Button(text="Try Again", command=reset_game)
reset_button.place(x=705, y=212)


# ---------------------------- RESULTS ------------------------------- #
def see_results():
    # Result Labels
    correct_results = Label(text=f"Results: {len(ENTRIES)} words per minute.",
                            font=(FONT_NAME, 18, "bold"), bg=BLACK, fg=WHITE, wraplength=800)
    correct_results.place(x=200, y=725)

    incorrect_results = Label(text=f"Misspelled results: {INCORRECT_WORDS}",
                              font=(FONT_NAME, 18, "bold"), bg=BLACK, fg=WHITE, wraplength=800)
    incorrect_results.place(x=30, y=775)


# Button to print entries
results_button = Button(text="Results", command=see_results)
results_button.place(x=650, y=212)

window.mainloop()
