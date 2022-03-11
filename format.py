import os
import random

def format_cardname(unf_cardname):
    # formats a cardname to desired format
    cardname = unf_cardname.replace(" ", "_")
    cardname = cardname.replace("'", "").replace(",", "")
    cardname = cardname.replace("-", "")
    cardname = cardname.replace("//", "_")
    cardname = cardname.lower()
    return(cardname)


def main():
    singles = []
    unf_lists_path = os.path.join(os.getcwd(), "unf_lists")
    f_lists_path = os.path.join(os.getcwd(), "f_lists")
    unf_lists_folder = os.scandir(unf_lists_path)
    
    # loops over archetypes
    for archetype in unf_lists_folder:
        archetype_folder = os.scandir(archetype.path)
        archetype_name = archetype.name
        # loops over decklists of that archetype
        for decklist in archetype_folder:
            decklist_name = decklist.name
            decklist_name = decklist_name.rstrip(".txt")
            cards = []
            # formats every card of the decklist
            with open(decklist.path, "r") as r:
                for line in r:
                    line = line.rstrip("\n")
                    if len(line) == 0:
                        continue
                    num = line[0:line.find(" ")]
                    unf_cardname = line[line.find(" ")+1:]
                    #cardname = format_cardname(unf_cardname)
                    if unf_cardname not in singles:
                        singles.append(unf_cardname)
                    for i in range(int(num)):
                        cards.append(unf_cardname)
    

            """
            # randomize the list
            len_list = len(cards)
            cards.sort(key=lambda c: random.randrange(len_list))

            # append formated list to new path
            f_archetype_path = f"{f_lists_path}{os.sep}{archetype_name}"

            
            # creates archetype if it's the first list of the archetype
            if decklist_name == "0":
                try:
                    os.mkdir(f_archetype_path)
                except Exception as e:
                    print("exception: ", e.__class__)

            f_decklist_path = f_archetype_path + f"{os.sep}{decklist_name}.txt"

            with open(f_decklist_path, "w") as w:
                for card in cards:
                    w.write(card)
                    w.write("\n")
            """
    # once all lists have been looked at, add all singles to a file
    with open("uf_singles.txt", "w") as w:
        for card in singles:
            w.write(card)
            w.write("\n")

if __name__ == "__main__":
    main()