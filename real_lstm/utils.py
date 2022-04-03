import os
import numpy as np

def load_data(path_to_decks):
    """
    returns a list of lists (decks(cards))
    """
    lists = []
    lists_folder = os.scandir(path_to_decks)
    # for each archetype, for each deck, load all cards into a list (list of decks (list of cards))
    for archetype in lists_folder:
        archetype_folder = os.scandir(archetype.path)
        # loops over decklists of that archetype
        for decklist in archetype_folder:
            cards = []
            # loads every card of the decklist
            with open(decklist.path, "r") as r:
                for line in r:
                    cardname = line.rstrip("\n")
                    if len(line) == 0:
                        continue
                    #appending vector, not cardname
                    cards.append(cardname)
            # only keep length 60 lists
            if(len(cards) == 60):
                lists.append(cards)
            else:
                lists.append(cards[:60])
    return(lists)


def split_data(data):
    """
    takes a list of decklists "data" as input
    returns 3 lists of decklists: train, test, val
    """
    train_data = []
    test_data = []
    val_data = []

    # frequencies at which data is appended to test and val
    # for example, [5, 40] means that 1/5 lists go in test, and 1/40 lists go in val
    test_f, val_f = 5, 40

    for index, decklist in enumerate(data):
        if index%val_f == 0:
            val_data.append(decklist)
        elif index%test_f == 0:
            test_data.append(decklist)
        else:
            train_data.append(decklist)
    return(train_data, test_data, val_data)

def main():
    path_to_lists = os.path.join(os.getcwd(), f"..{os.sep}f_lists")
    data = load_data(path_to_lists)
    train_data, test_data, val_data = split_data(data)
    



if __name__ == "__main__":
    main()