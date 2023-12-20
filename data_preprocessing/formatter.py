import os
import random
from typing import List, Tuple

from config import PATH_TO_UNFORMATTED_DECKLIST_DIR, PATH_TO_FORMATTED_DECKLIST_DIR, PATH_TO_FORMATTED_UNIQUE_CARDNAMES


def format_all_decklists() -> None:
    unique_formatted_cardnames = set()
    for unformatted_archetype_dir in os.scandir(PATH_TO_UNFORMATTED_DECKLIST_DIR):
        archetype_name = unformatted_archetype_dir.name
        path_to_unformatted_archetype_dir = unformatted_archetype_dir.path
        path_to_formatted_archetype_dir = get_path_to_formatted_archetype_dir(archetype_name)
        format_decklists_in_archetype_dir(path_to_formatted_archetype_dir, path_to_unformatted_archetype_dir,
                                          unique_formatted_cardnames)
    save_unique_cardnames(unique_formatted_cardnames, PATH_TO_FORMATTED_UNIQUE_CARDNAMES)


def format_decklists_in_archetype_dir(path_to_formatted_archetype_dir: str, path_to_unformatted_decklist_dir: str,
                                      unique_formatted_cardnames: set) -> None:
    ensure_dir_exists(path_to_formatted_archetype_dir)
    for unformatted_decklist_file in os.scandir(path_to_unformatted_decklist_dir):
        print(f"formatting: {unformatted_decklist_file.path}")
        formatted_decklist = get_formatted_decklist(unformatted_decklist_file.path)
        unique_formatted_cardnames.update(formatted_decklist)
        randomize_decklist(formatted_decklist)
        path_to_formatted_decklist = get_path_to_formatted_decklist(path_to_formatted_archetype_dir,
                                                                    unformatted_decklist_file.name)
        save_decklist_to_path(formatted_decklist, path_to_formatted_decklist)


def save_unique_cardnames(unique_cardnames: set, path_to_unique_cardnames: str) -> None:
    sorted_unique_cardnames = sorted(unique_cardnames)
    unique_cardnames_string = '\n'.join(sorted_unique_cardnames)
    with open(path_to_unique_cardnames, 'w') as unique_cardnames_file:
        unique_cardnames_file.write(unique_cardnames_string)


def get_path_to_formatted_archetype_dir(archetype_name: str) -> str:
    return os.path.join(PATH_TO_FORMATTED_DECKLIST_DIR, archetype_name)


def get_path_to_formatted_decklist(path_to_formatted_archetype_dir: str, decklist_name: str) -> str:
    return os.path.join(path_to_formatted_archetype_dir, decklist_name)


def ensure_dir_exists(path_to_dir: str) -> None:
    os.makedirs(path_to_dir, exist_ok=True)


def save_decklist_to_path(decklist: List[str], path_to_formatted_decklist: str) -> None:
    decklist_as_string = '\n'.join(decklist)
    with open(path_to_formatted_decklist, "w") as w:
        w.write(decklist_as_string)


def randomize_decklist(formatted_decklist: List[str]) -> None:
    len_formatted_decklist = len(formatted_decklist)
    formatted_decklist.sort(key=lambda c: random.randrange(0, len_formatted_decklist, 1))


def get_formatted_decklist(path_to_decklist_file: str) -> List[str]:
    formatted_decklist = []
    with open(path_to_decklist_file, "r") as r:
        for line in r:
            num_copies, unformatted_cardname = parse_unformatted_line(line)
            if num_copies <= 0:  # empty line: skip sideboard
                break
            formatted_cardname = format_cardname(unformatted_cardname)
            add_num_copies_of_card_to_decklist(num_copies, formatted_cardname, formatted_decklist)
    return formatted_decklist


def add_num_copies_of_card_to_decklist(num: int, formatted_cardname: str, decklist: List[str]) -> None:
    for i in range(num):
        decklist.append(formatted_cardname)


def parse_unformatted_line(unformatted_line: str) -> Tuple[int, str]:
    unformatted_line = unformatted_line.rstrip("\n")
    num_copies = get_num_copies_from_unparsed_line(unformatted_line)
    unformatted_cardname = unformatted_line[unformatted_line.find(" ") + 1:]
    return num_copies, unformatted_cardname


def get_num_copies_from_unparsed_line(unformatted_line: str) -> int:
    num_copies_string = unformatted_line[0:unformatted_line.find(" ")]
    try:
        num_copies = int(num_copies_string)
    except ValueError:
        num_copies = 0
    return num_copies


def format_cardname(unformatted_cardname: str) -> str:
    cardname = replace_symbols_by_symbol([","], unformatted_cardname, "")
    cardname = replace_symbols_by_symbol(["//", "'", " ", "-"], cardname, "_")
    cardname = cardname.lower()
    return cardname


def replace_symbols_by_symbol(symbols_to_replace: List[str], string: str, target_symbol) -> str:
    for symbol in symbols_to_replace:
        string = string.replace(symbol, target_symbol)
    return string


if __name__ == "__main__":
    format_all_decklists()
