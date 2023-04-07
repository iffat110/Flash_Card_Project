from tkinter import *
import pandas
import random
current_card = {}
to_learn = {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(language_text, text="French", fill="Black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="Black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(language_text, text="English", fill="White")
    canvas.itemconfig(word_text, text=current_card["English"], fill="White")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flashy")
window.config(padx=80, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
language_text = canvas.create_text(400, 215, text="", fill="black", font=("Ariel", 30, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 50, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
button = Button(image=right_image, command=is_known, highlightthickness=0)
button.grid(row=1, column=1)
button = Button(image=wrong_image, command=next_card, highlightthickness=0)
button.grid(row=1, column=0)

next_card()


window.mainloop()

