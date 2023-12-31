import os
from typing import List

from gensim.models import Word2Vec

from config import PATH_TO_FORMATTED_DECKLIST_DIR, PATH_TO_W2V_MODELS_DIR


def vectorize_cardnames():
    path_to_w2v_model = os.path.join(PATH_TO_W2V_MODELS_DIR, "w2v_31_12_2023.model")

    lists = get_all_decklists(PATH_TO_FORMATTED_DECKLIST_DIR)
    model = Word2Vec(lists, min_count=1, vector_size=64, epochs=10)
    model.save(path_to_w2v_model)


def get_all_decklists(path_to_decklists_dir: str) -> List[List[str]]:
    lists = []
    for archetype in os.scandir(path_to_decklists_dir):
        for decklist in os.scandir(archetype.path):
            cards = []
            with open(decklist.path, "r") as r:
                for line in r:
                    cardname = line.rstrip("\n")
                    if len(line) == 0:
                        continue
                    cards.append(cardname)
            lists.append(cards)
    return lists


if __name__ == "__main__":
    vectorize_cardnames()
