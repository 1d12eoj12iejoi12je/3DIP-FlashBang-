import tkinter as tk
from tkinter import messagebox, simpledialog

"""
This is the second version of my Flashcard program. The program will allow user to create, and study their decks to help
students and other to memorise content for test and other purposes.
"""


# ======= CLASSES ========
class Deck:  # Deck class to create new decks
    def __init__(self, title, items):
        self.title = title
        self.items = items

    def add_deck(self):  # function to add a new deck to the dictionary
        if self.title and self.items:
            decks.update({self.title: self.items})


class Cards:  # Cards class to store all information about the deck
    def __init__(self, top, bottom, name, studying_deck, new_front):
        self.top = top
        self.bottom = bottom
        self.name = name
        self.studying_deck = studying_deck
        self.new_front = new_front

    def add_card(self):  # Function to add a card to the deck
        decks.get(self.name).update({self.new_front: self.bottom})
        logic_loop(self.name)
        messagebox.showinfo("Success", "Card Added!")

    def edit_card(self):  # Function to edit the current card in the deck
        decks.get(self.name).pop(self.top)
        decks.get(self.name).update({self.new_front: self.bottom})
        logic_loop(self.name)
        messagebox.showinfo("Success", "Card Edited!")


# ======= FUNCTIONS ========
def show_frame(frame):  # function to switch between frames e.g. menu, deck and studying frame
    for f in (menu_frame, deck_frame, study_frame):
        f.pack_forget()  # hides all frames
    frame.pack(fill="both", expand=True)  # shows needed frame and fills to size of window and can be expanded


def logic_loop(name):  # function controls logic of program
    global current_deck, study_deck, current_cards, current_index, showing_front
    current_deck = name
    study_deck = decks.get(name)
    current_cards = list(decks[name].items())
    current_index = 0
    showing_front = True
    if not current_cards:  # if the deck is empty
        messagebox.showinfo("Empty Deck", "This deck has no cards!")
        return
    deck_config()
    show_frame(study_frame)


def deck_config():  # function to display front and back of cards on studying frame
    card_label.config(text=f"Front: \n{current_cards[current_index][0]}"
    if showing_front else f"Back: \n"f"{current_cards[current_index][1]}")


def select_deck():  # function to create the select deck screen
    for widget in deck_frame.winfo_children():
        widget.destroy()  # destroys previous buttons, so it can be updated with new decks
    tk.Label(deck_frame, text="Select a Deck", font=("Ariel", 14)).pack(pady=10)
    for d in decks:
        tk.Button(deck_frame, text=d.title(), command=lambda name=d: logic_loop(name)).pack(pady=10)
    tk.Button(deck_frame, text="Menu", command=lambda: show_frame(menu_frame)).pack(pady=10)


def add_deck():  # function to add a new deck
    mini_deck = {}  # empty dictionary used to append to main 3D dictionary
    deck_name = simpledialog.askstring("Deck Name", "Enter deck name (cancel or leave blank to stop):\t\t\t\t")
    if deck_name is None:  # if the user presses cancel
        return
    if deck_name.strip() == "":  # if the user leaves field blank
        messagebox.showinfo("Cancel!", "Field left blank!\nCanceling action!")
        return
    while True:
        front = simpledialog.askstring("Enter Cards",
                                       "Enter text for front of card (cancel to stop):\t\t\t\t")
        if front is None:  # if the user presses cancel
            messagebox.showinfo("Deck Added!", "Deck has been added!")
            return
        if front.strip() == "":  # if the user leaves field blank
            messagebox.showinfo("Error!", "Please enter text!")
            continue
        else:
            while True:
                back = simpledialog.askstring("Enter Cards", "Enter text for back of card:\t\t\t\t\t\t")
                if back is None:  # if the user presses cancel
                    messagebox.showinfo("Error!", "Please enter text!")
                elif back.strip() == "":  # if the user leaves field blank
                    messagebox.showinfo("Error!", "Please enter text!")
                else:
                    break
            mini_deck.update({front: back})
        Deck(deck_name, mini_deck).add_deck()  # instantiating object and calling add_deck function


def flip():  # Function to flip the card to show back or front
    global showing_front
    showing_front = not showing_front
    deck_config()  # to update what is being displayed on the screen


def edit_card():  # function to edit the current card
    while True:
        front = simpledialog.askstring("Edit Card", "Enter text for front of card: \t\t\t\t")
        back = simpledialog.askstring("Edit Card", "Enter text for back of card: \t\t\t\t")
        if front.strip() and back.strip():  # both front and back should be filled
            Cards(current_cards[current_index][0], back, current_deck, None, front).edit_card()
            # instantiating Cards object and calling edit_card function
            break
        else:
            messagebox.showinfo("Error!", "Please enter text for back and front!")


def add_card():  # function to add card to current deck
    while True:
        front = simpledialog.askstring("Add Card", "Enter text for front of card: \t\t\t\t")
        back = simpledialog.askstring("Add Card", "Enter text for back of card: \t\t\t\t")
        if front and back:  # both front and back should be filled
            Cards(None, back, current_deck, None, front).add_card()
            # instantiating Cards object and calling add_card function
            break
        else:
            messagebox.showinfo("Error!", "Please enter text for back and front!")


def next_card():  # function to move to next card
    global current_index, showing_front
    if not current_cards:
        return
    current_index = (current_index + 1) % len(current_cards)  # logic keeps index inside valid range
    showing_front = True
    deck_config()  # to update what is being shown on screen


def delete_card():  # function to delete card
    global current_cards, current_index, current_deck
    front, back = current_cards[current_index]
    del decks[current_deck][front]  # deleting from main dictionary
    current_cards = list(decks[current_deck].items())  # updating list of cards
    if not current_cards:  # if the deck is empty
        messagebox.showinfo("Empty Deck!", f"Deck '{current_deck}' is empty!")
        show_frame(deck_frame)  # back to select deck frame
        del decks[current_deck]  # delete the deck from the dictionary
        current_deck = ""  # reset variable
        select_deck()  # reset decks and show select deck frame
        return
    current_index %= len(current_cards)  # ensuring index within range
    deck_config()  # to update screen
    messagebox.showinfo("Success!", "Card deleted!")


# ======= GLOBALS/CONSTANTS =======
# dictionary storing all the decks in a 3D dictionary
decks = {
    "animal sounds": {"pig": "oink", "dog": "woof", "cat": "meow"},
    "chemical symbols": {"Sodium": "Na", "Oxygen": "O", "Chlorine": "Cl", "Lead": "Pb", "Carbon": "C"}
}
current_deck = ""
study_deck = None
current_cards = []
current_index = 0
showing_front = True

# ======= GUI APP ========
root = tk.Tk()
root.title("FlashBang!")
root.geometry("500x400")

# ======= FRAMES ========
menu_frame = tk.Frame(root)
deck_frame = tk.Frame(root)
study_frame = tk.Frame(root)

# ======= MENU SCREEN ========
tk.Label(menu_frame, text="Welcome to\nFlashBang", font=("Ariel", 18)).pack(pady=20)
tk.Button(menu_frame, text="Select Deck", command=lambda: [select_deck(), show_frame(deck_frame)]).pack(pady=20)
tk.Button(menu_frame, text="Add deck", command=lambda: add_deck()).pack(pady=15)
tk.Button(menu_frame, text="Exit", command=root.destroy).pack(pady=20)

# ======= STUDY SCREEN ========
card_label = tk.Label(study_frame, text="", font=("Ariel", 16))
card_label.pack(pady=30)

btn_frame = tk.Frame(study_frame)
btn_frame.pack(pady=40)

tk.Button(btn_frame, text="Flip Card", command=flip).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Next Card", command=next_card).grid(row=0, column=1, padx=5)

tk.Button(study_frame, text="Add Card", command=lambda: add_card()).pack(padx=5, pady=7)
tk.Button(study_frame, text="Edit Card", command=lambda: edit_card()).pack(padx=5, pady=7)
tk.Button(study_frame, text="Delete Card", command=lambda: delete_card()).pack(padx=5, pady=7)
tk.Button(study_frame, text="Menu", command=lambda: [show_frame(menu_frame)]).pack(padx=5, pady=7)

# starting with menu
show_frame(menu_frame)
root.mainloop()
