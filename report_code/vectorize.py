import os
from gensim.models import Word2Vec


def main():
    lists = []
    f_lists_path = os.path.join(os.getcwd(), "f_lists")
    f_lists_folder = os.scandir(f_lists_path)
    
    # this bit loads all the cards into memory
    # loops over archetypes
    for archetype in f_lists_folder:
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
                    cards.append(cardname)
            lists.append(cards)
    
    # this is the line that vectorizes all the card "vocabulary"
    # I had not expected it to be that easy...
    model = Word2Vec(lists, min_count=1, vector_size=64, epochs=10)
    model.save("w2v_models/m3.model")
            

if __name__ == "__main__":
    main()