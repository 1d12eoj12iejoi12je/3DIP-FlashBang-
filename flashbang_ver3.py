import tkinter as tk
import random
import os
import json
import tkinter.font as tf
from tkinter import messagebox, simpledialog

"""
This is the fourth version of my Flashcard program. The program will allow user to create, and study their decks to help
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
            save_decks()  # saves deck to json file


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
        save_decks()  # saves deck to json file

    def edit_card(self):  # Function to edit the current card in the deck
        decks.get(self.name).pop(self.top)
        decks.get(self.name).update({self.new_front: self.bottom})
        logic_loop(self.name)
        messagebox.showinfo("Success", "Card Edited!")
        save_decks()  # save deck to file


# ======= FUNCTIONS ========
def show_frame(frame):  # function to switch between frames e.g. menu, deck and studying frame
    global current_deck
    for f in (menu_frame, deck_frame, study_frame):
        f.pack_forget()  # hides all frames
    frame.pack(fill="both", expand=True)  # shows needed frame and fills to size of window
    if frame == study_frame:
        study_frame.focus_set()  # ensure key bindings work on study screen
    else:
        current_deck = None  # resetting current deck so users cannot edit cards in different frames


def logic_loop(name):
    """
    This function controls the logic of the program. Variables are set as global so other functions can use these
    updated values to ensure the program runs as expected. This function sets up the global variables used as logic.
    """
    global current_deck, study_deck, current_cards, current_index, showing_front
    current_deck = name
    study_deck = decks.get(name)
    current_cards = list(decks[name].items())
    current_index = 0  # start on card 1
    showing_front = True  # always start on front
    if not current_cards:  # if the deck is empty
        messagebox.showinfo("Empty Deck", "This deck has no cards!")
        return
    deck_config()
    show_frame(study_frame)


def deck_config():
    """
    This function controls what is being displayed on the study screen. When a card is flipped or another card is
    selected it updates the display to show the new information including the card number, deck name, and if front or
    back is being shown.
    """
    deck_name.config(text=current_deck.title())  # show deck name
    card_info.config(text=f"{current_index+1} of {len(current_cards)}")  # show card number
    if showing_front:
        card_label.config(text=f"{current_cards[current_index][0]}")
    else:
        card_label.config(text=f"{current_cards[current_index][1]}")

    if showing_front:
        side_label.config(text="Front")
    else:
        side_label.config(text="Back")


def select_deck():
    """
    This function creates the select deck frame. It destroys the previous frame and makes a new one using the decks
    from the dictionary. Furthermore, it ensures that the frame is scrollable so if many decks are added the user can
    scroll through them.
    """
    for widget in deck_frame.winfo_children():
        widget.destroy()  # destroys previous buttons, so it can be updated with new decks
        
    tk.Label(deck_frame, text="📚 Select a Deck!", font=("Ariel", 24, "bold")).pack(pady=20)
    # Make the frame scrollable
    global scroll_deck_frame
    scroll_deck_frame = make_scrollable_frame(deck_frame)

    for d in decks:  # making button for each deck in dictionary
        tk.Button(scroll_deck_frame, font=my_font, text=d.title(), bd=3, width=15, height=3,
                  command=lambda name=d: logic_loop(name)).pack(pady=10)
    tk.Button(scroll_deck_frame, text="🏠 Home", font=my_font, bd=3, width=15, height=3,
              command=lambda: show_frame(menu_frame)).pack(pady=10)


def add_deck():
    """
    This function allows users to add new decks by taking input from the user and ensuring it is valid by running it
    through a validator function.
    """
    mini_deck = {}

    while True:  # loop continues until cancel is pressed or valid input obtained
        name = validator(simpledialog.askstring("Deck Name!", "Enter name of deck:\t\t\t\t"), "Deck Name")
        # calling function to validify input
        if name is None:  # user presses cancel
            return
        if name.lower() in decks:
            messagebox.showerror("Error!", "Ths deck already exists!")
            continue
        if name:  # valid input
            break

    while True:  # loop continues until cancel is pressed
        # calling function to validify input
        front = validator(simpledialog.askstring("New Card!", "Enter text for front of card (press cancel to "
                                                              "finish adding cards):\t\t"), "Front of Card")
        if front is None:  # user presses cancel
            Deck(name.lower(), mini_deck).add_deck()  # instantiating object and calling add_deck function
            messagebox.showinfo("Success!", "Deck added!")
            return
        if not front:  # invalid input
            continue

        back = validator(simpledialog.askstring("New Card!", "Enter text for back of card\t\t\t\t"), "Back of Card")
        if back is None:  # cancel --> don't save this card
            return
        if not back:  # invalid input
            continue

        mini_deck.update({str(front): str(back)})


def flip():  # Function to flip the card to show back or front
    global showing_front
    showing_front = not showing_front
    deck_config()  # to update what is being displayed on the screen


def validator(user_input, field_name):
    """
    Validates user input from simpledialog.askstring.
    Returns the stripped input if valid, None otherwise.
    """
    if user_input is None:  # user pressed cancel
        return None

    user_input = user_input.strip()  # remove spaces before and after

    if not user_input:  # empty after stripping spaces
        messagebox.showerror("Error!", f"{field_name} cannot be empty or spaces only!")
        return ""
    else:
        return user_input


def edit_card():
    """
    Function to edit the current card the user is on. Takes input and runs through validator function before updating
    card.
    """
    if not current_deck:  # if user edits deck before a deck has been selected
        messagebox.showerror("Error!", "No deck selected!")
        return
    while True:  # loop continues until cancel is pressed or valid input obtained
        front = validator(simpledialog.askstring("Edit Card!", "Enter text for front of card:\t\t\t\t"),
                          "Front of Card")  # calling function to validify input
        if front is None:  # user presses cancel
            return
        if front:  # valid input
            break

    while True:  # loop continues until cancel is pressed or valid input obtained
        # calling function to validify input
        back = validator(simpledialog.askstring("Edit Card!", "Enter text for back of card:\t\t\t\t"), "Back of Card")
        if back is None:  # user presses cancel
            return
        if back:  # valid input
            break
    # Update card by instantiating object and called edit card method
    Cards(current_cards[current_index][0], back, current_deck, None, front).edit_card()


def random_card():
    """
    Function uses random module to select a random index with the range of the deck to display a random card.
    """
    global current_index, showing_front  # global variables so other functions can use new values
    if not current_cards:  # if no deck selected
        return
    current_index = random.randrange(len(current_cards))  # selects random index using random module
    showing_front = True  # always shows front first
    deck_config()  # updates display


def add_card():
    if not current_deck:
        messagebox.showerror("Error!", "No deck selected!")
        return

    while True:
        front = validator(simpledialog.askstring("Add Card!", "Enter text for front of card:\t\t\t\t"), "Front of Card")
        if front is None:  # cancel or invalid input
            return
        if front:  # valid input
            break

    while True:
        back = validator(simpledialog.askstring("Add Card!", "Enter text for back of card:\t\t\t\t"), "Back of Card")
        if back is None:  # cancel or invalid input
            return
        if back:  # valid input
            break

    Cards(None, back, current_deck, None, front).add_card()


def next_card():  # function to move to next card
    global current_index, showing_front  # global variables so other functions can use new values
    if not current_cards:  # no deck selected
        messagebox.showerror("Error!", "No deck selected!")
        return
    current_index = (current_index + 1) % len(current_cards)  # logic keeps index inside valid range
    showing_front = True  # show front first
    deck_config()  # to update what is being shown on screen


def prev_card():  # function to move to previous card
    global current_index, showing_front  # global variables so other functions can use new values
    if not current_cards:  # no deck selected
        return
    current_index = (current_index - 1) % len(current_cards)  # logic keeps index inside valid range
    showing_front = True  # show front first
    deck_config()  # to update what is being shown on screen


def delete_card():
    """
    Function to delete the current card user is on. If the deck is then empty, the function will also delete the deck.
    """
    global current_cards, current_index, current_deck  # global variables so other functions can use new values
    if not current_deck:  # no deck selected
        messagebox.showerror("Error!", "No deck selected!")
        return
    front, back = current_cards[current_index]
    del decks[current_deck][front]  # deleting from main dictionary
    current_cards = list(decks[current_deck].items())  # updating list of cards
    if not current_cards:  # if the deck is NOW empty
        messagebox.showinfo("Empty Deck!", f"Deck '{current_deck}' is empty!")
        show_frame(deck_frame)  # back to select deck frame
        del decks[current_deck]  # delete the deck from the dictionary
        save_decks()  # saves deck to json file
        current_deck = ""  # reset variable
        select_deck()  # reset decks and show select deck frame
        return
    current_index %= len(current_cards)  # ensuring index within range
    deck_config()  # to update screen
    messagebox.showinfo("Success!", "Card deleted!")
    save_decks()  # saves deck to json file


def load_decks():
    """Load decks from JSON file or return empty dict if not found/invalid."""
    if os.path.exists(DECKS_FILE):  # checking if file location exists
        try:
            with open(DECKS_FILE, "r") as f:
                data = f.read().strip()  # reads file and strips extra spaces
                if not data:  # file is empty
                    return {}  # returns empty dictionary
                return json.loads(data)  # loads existing decks into dictionary form
        except json.JSONDecodeError:  # file exists but has invalid JSON
            return {}  # returns empty dictionary
    return {}  # returns empty dictionary


def save_decks():  # function to save deck after adding/editing deck
    """saves current decks to jason file including any changes made"""
    with open(DECKS_FILE, "w") as f:  # opens file to overwrite content and closes when done
        json.dump(decks, f, indent=4)  # adds new dictionary, file and indents for easy reading


def make_scrollable_frame(container):
    """
    Function to create a canvas inside a frame so that a scrollbar can be added that can scroll through the buttons.
    Scrolling is bound to moving the scroll wheel.
    """
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(  # Every time the frame’s size changes, this updates the scrollable area of the canvas.
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # keep scrollable_frame width synced with canvas width to ensure buttons are center aligned
    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig("inner_frame", width=e.width)
    )

    # Place scrollable_frame inside canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n", tags="inner_frame")
    canvas.configure(yscrollcommand=scrollbar.set)  # Makes the scrollbar reflect the canvas scrolling.

    canvas.pack(side="left", fill="both", expand=True)  # takes all horizontal space
    scrollbar.pack(side="right", fill="y")  # sits on right and fills vertical space

    def _on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    return scrollable_frame


# ======= GLOBALS/CONSTANTS =======
# location of json file storing decks
DECKS_FILE = "decks.json"
decks = load_decks()  # adding existing decks to dictionary

# If empty, adds some default decks:
if not decks:
    decks.update({
        "animal sounds": {"pig": "oink", "dog": "woof", "cat": "meow"},
        "chemical symbols": {"Sodium": "Na", "Oxygen": "O", "Chlorine": "Cl", "Lead": "Pb", "Carbon": "C"}
    })
    save_decks()  # saves deck to json file
current_deck = ""
study_deck = None
current_cards = []
current_index = 0
showing_front = True

# ======= GUI APP ========
root = tk.Tk()
root.title("FlashBang!")
root.geometry("500x400")
my_font = tf.Font(family="Arial", size=10)

# ======= FRAMES ========
menu_frame = tk.Frame(root)
study_frame = tk.Frame(root)
deck_frame = tk.Frame(root)
scroll_deck_frame = make_scrollable_frame(deck_frame)

# ======= MENU SCREEN ========
tk.Label(menu_frame, text="⚡ FlashBang!", font=("Ariel", 24, "bold")).pack(pady=10)
tk.Label(menu_frame, text="Learning in a Flash!", font=("Ariel", 14, "italic")).pack(pady=20)
tk.Button(menu_frame, text="📂 Select Deck", font=my_font, bd=3, width=20, height=3,
          command=lambda: [select_deck(), show_frame(deck_frame)]).pack(pady=10, padx=20)
tk.Button(menu_frame, text="➕ Add deck", font=my_font, width=20, bd=3, height=3,
          command=lambda: add_deck()).pack(pady=10, padx=20)
tk.Button(menu_frame, text="🚪 Exit", bd=3, font=my_font, width=20, height=3,
          command=root.destroy).pack(pady=10, padx=20)

# ======= STUDY SCREEN ========
# Configure study_frame grid
study_frame.rowconfigure(1, weight=1)   # <-- middle row expands
for col in range(3):
    study_frame.columnconfigure(col, weight=1, uniform="nav")

deck_name = tk.Label(study_frame, text="", font=("Ariel", 10))
deck_name.grid(row=0, column=0, sticky="w", padx=5)

card_info = tk.Label(study_frame, text="", font=("Ariel", 10))
card_info.grid(row=0, column=2, sticky="e", padx=5)

card_label = tk.Label(study_frame, text="", font=("Ariel", 16))
card_label.grid(row=1, column=0, columnspan=3, pady=20)

side_label = tk.Label(study_frame, text="Front", font=("Ariel", 10, "italic"), fg="gray")
side_label.grid(row=0, column=1, pady=5)

tk.Button(study_frame, text="⚡ Flip Card", bd=3, font=my_font, command=flip).grid(row=2, column=0, columnspan=3,
                                                                                  pady=10, padx=10, sticky="ew")

tk.Button(study_frame, text="<<<", command=prev_card, font=my_font, bd=3).grid(row=3, column=0, padx=10, sticky="nsew")
tk.Button(study_frame, text="Random", bd=3, font=my_font, command=lambda: random_card()).grid(row=3, column=1, padx=10,
                                                                                              sticky="nsew")
tk.Button(study_frame, text=">>>", bd=3, font=my_font, command=next_card).grid(row=3, column=2, padx=10, sticky="nsew")

tk.Button(study_frame, text="🏠 Menu", bd=3, font=my_font, command=lambda: [show_frame(menu_frame)]).grid(
    row=4, column=0, padx=10, pady=5, sticky="ew", columnspan=3)

# ======= MENU BAR ========
menubar = tk.Menu(root)  # creating menu
root.config(menu=menubar)  # attaching menubar to root window
edit_menu = tk.Menu(menubar, tearoff=0)  # disables dashed line for window
menubar.add_cascade(label="Edit", menu=edit_menu)  # adding edit to menubar

edit_menu.add_command(label="Add Card", command=add_card)  # option to add card
edit_menu.add_command(label="Edit Card", command=edit_card)  # option to edit card
edit_menu.add_command(label="Delete Card", command=delete_card)  # option to delete card

help_menu = tk.Menu(menubar, tearoff=0)  # disables dashed line for window
menubar.add_cascade(label="Help", menu=help_menu)  # adding help to menu bar
help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
    "About?",
    "FlashBang!\nYour flashcard study tool.\n"
    "Main Menu:\n"
    "\tAdd Deck – Create a new deck.\n"
    "\tView Decks – Open or edit an existing deck.\n"
    "\tExit – Close the program.\n"
    "Deck Screen:\n"
    "\tAdd Card – Add a new flashcard.\n"
    "\tEdit/Delete Card – Change or remove a card.\n"
    "\tStudy Deck – Start studying your cards.\n"
    "Study Screen:\n"
    "\tSpacebar – Flip the card.\n"
    "\tArrow Keys – Move between cards.\n"
    "Tips:\n"
    "\tAvoid empty names or cards.\n"
    "\tDecks save automatically.\n"
    "\tKeep names short and simple!"))
# ====== BINDS =======
study_frame.bind("<space>", lambda event: flip())
study_frame.bind("<Left>", lambda event: prev_card())
study_frame.bind("<Right>", lambda event: next_card())
# Make sure the frame can receive key events
study_frame.focus_set()

show_frame(menu_frame)  # starting with menu
root.mainloop()


