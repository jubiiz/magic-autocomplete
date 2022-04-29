import os

from metadata import F_LISTS_DIR, F_SINGLES_PATH


def load_f_singles() -> list[str]:
    """loads the card vocabulary: a list of unique cardnames"""
    _f_singles = ['padding_cardname']
    with open(F_SINGLES_PATH) as f:
        for single in f:
            _f_singles.append(single.strip('\n'))
    return _f_singles


def load_unf_singles():
    # TODO
    pass


def nums_to_cardnames(nums: list[int]) -> list[str]:
    """input a list of card INDEXES, outputs a list of FORMATTED cardnames"""
    return [F_SINGLES[index] for index in nums]


def cardnames_to_nums(cards: list[str]) -> list[int]:
    """input a list of FORMATTED cardnames, outputs a list of ints"""
    return [F_SINGLES.index(cardname) for cardname in cards]


def load_decklists() -> list[list[int]]:
    """
    loads all formatted decklists as a list of lists of numbers
    """
    decklists = []
    f_lists_dir = os.scandir(F_LISTS_DIR)
    for archetype_obj in f_lists_dir:
        archetype_dir = os.scandir(archetype_obj.path)
        for decklist_obj in archetype_dir:
            decklist = []
            with open(decklist_obj.path, "r") as f:
                for line in f:
                    cardname = line.rstrip("\n")
                    if len(line) == 0:
                        continue
                    decklist.append(cardname)

                # only keep length 60 lists
                # (we don't also want to have to predict the size of the list)
                if len(decklist) == 60:
                    decklists.append(cardnames_to_nums(decklist))
                else:
                    decklists.append(cardnames_to_nums(decklist))
    return decklists


F_SINGLES = load_f_singles()
# UNF_SINGLES = load_unf_singles()

if __name__ == "__main__":
    load_decklists()
