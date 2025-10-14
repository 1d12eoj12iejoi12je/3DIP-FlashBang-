"""
This is the first version of my Flashcard program. The program will allow user to create, and study their decks to help
students and other to memorise content for test and other purposes.
"""


class Deck:  # Deck class to create new decks
    def __init__(self, title, items):
        self.title = title
        self.items = items

    def add_deck(self):  # function to add a new deck to the dictionary
        decks.update({self.title: self.items})


class Cards:  # Cards class to store all information about the deck
    def __init__(self, top, bottom, name, studying_deck, new_front):
        self.top = top
        self.bottom = bottom
        self.name = name
        self.studying_deck = studying_deck
        self.new_front = new_front

    def flip(self):  # Function to show back of card (flip)
        print("Back: {}".format(self.studying_deck.get(self.top)))

    def delete_card(self):  # Function to delete current card
        print("Card deleted!")
        decks.get(self.name).pop(self.top)
        print(decks)
        if not self.studying_deck:
            decks.pop(self.name)
            print("'{}' is empty".format(self.name.title()))
            return True

    def add_card(self):  # Function to add a card to the deck
        decks.get(self.name).update({self.new_front: self.bottom})
        print("Card added!")

    def edit_card(self):  # Function to edit the current card in the deck
        decks.get(self.name).pop(self.top)
        decks.get(self.name).update({self.new_front: self.bottom})
        print("Card updated!")


# dictionary storing all the decks in a 3D dictionary
decks = {
    "animal sounds": {"pig": "oink", "dog": "woof", "cat": "meow"},
    "chemical symbols": {"Sodium": "Na", "Oxygen": "O", "Chlorine": "Cl", "Lead": "Pb", "Carbon": "C"}
         }
# defining variables
choice = 0
func = 0
front = ""
i = 0
mini_deck = {}
while True:  # Main loop
    while True:  # Inner loop
        loop_done = False  # Variable to exit the inner loop
        print("***************************")

        # Ensuring valid input for choice, must be integer smaller than 4 and larger than 0
        try:
            choice = int(input("Please enter function:\n1. Select deck\n2. Create new deck\n3. Exit\n: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        else:
            if 4 > choice > 0:
                break
            else:
                print("Please enter a valid number!")
                continue
    if choice == 3:  # exit app
        print("Thanks for using the app!")
        exit()

    elif choice == 2:  # add deck
        deck_name = input("Name of deck: ").lower()
        while True:
            front = input("Text for front of card: (type 'Exit' to stop): ").title()
            if front == "Exit":
                break
            else:
                back = input("Text for back of card: ")
                mini_deck.update({front: back})
        Deck(deck_name, mini_deck).add_deck()  # instantiating object and calling add deck function

    else:  # select deck
        if not decks:  # if the dictionary is empty
            print("You have no existing decks!")
            continue
        print("Decks:")
        for i in decks:
            print("\t"+i.title())  # printing existing decks
        while True:
            deck_select = input("Which deck would you like to select? ").lower()
            if deck_select not in decks.keys():  # checking if selected deck exists in dictionary
                print("This deck does not exist!")
                continue
            else:
                print("Deck Found")
                break
        study_deck = decks.get(deck_select)
        while not loop_done:
            for item in list(study_deck):  # iterating through items in the selected deck
                while True:
                    # ensuring input is valid as must be number above 0 and below 6
                    try:
                        print("***********************")
                        print("Front: {}".format(item))
                        func = int(input("Please enter function:\n1. Flip card\n2. Delete card\n3. Add card\n"
                                         "4. Edit card\n5. Exit\n: "))
                    except ValueError:
                        print("Please enter a valid number!")
                        continue
                    else:
                        if 6 > func > 0:
                            break
                        else:
                            print("Please enter a valid number!")
                            continue
                if func == 5:
                    loop_done = True  # breaking inner loop returning to main loop
                    break

                elif func == 1:
                    Cards(item, None, None, study_deck, None).flip()  # instantiating object and calling flip function

                elif func == 2:
                    del1 = Cards(item, None, deck_select, study_deck, None).delete_card()
                    # instantiating object and calling delete card function
                    if del1:
                        loop_done = True  # function returns True when deck's empty breaking inner loop to main function
                        break

                elif func == 3:
                    front = input("Text for front of card: ")
                    back = input("Test for back of card: ")
                    Cards(None, back, deck_select, study_deck, front).add_card()
                    # instantiating object and calling add card function

                elif func == 4:
                    front = input("Text for front of card: ")
                    back = input("Test for back of card: ")
                    Cards(item, back, deck_select, study_deck, front).edit_card()
                    # instantiating object and calling edit card function
