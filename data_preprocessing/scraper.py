import os
from typing import List

import urllib3
import requests
from bs4 import BeautifulSoup

MAX_LISTS_PER_ARCHETYPE = 5

PATH_TO_DATA_DIR = "data_18_12_2023"
PATH_TO_UNFORMATTED_DECKLIST_DIR = os.path.join(PATH_TO_DATA_DIR, "unformatted_decklists")
PATH_TO_LINKS_DIR = os.path.join(PATH_TO_DATA_DIR, "links")


def main():
    # name of the folder that will be created and contain the archetype of list current
    archetype_name = "mono_blue_tron"
    url_to_deck_page = "https://www.mtggoldfish.com/archetype/mono-blue-tron/decks" # there might be issues with the long weird name (try initial = one of the side ones)
    #https://www.mtggoldfish.com/archetype/modern-murktide-regent/decks
    #https://www.mtggoldfish.com/archetype/modern-murktide-regent#paper

    download_links = get_download_urls_for_one_archetype("https://www.mtggoldfish.com/archetype/mono-blue-tron/decks")
    log_download_links(archetype_name, download_links)


def get_download_urls_for_one_archetype(url_to_decks_page: str) -> List[str]:
    """
    Returns a list of all the download URLs. Each allows to download one text decklist.
    """
    individual_download_urls = []
    decks_page_html = requests.get(url_to_decks_page).text
    decks_page_soup = BeautifulSoup(decks_page_html, 'html.parser')
    decks_table = decks_page_soup.find('table', class_='table table-striped')
    return _extract_deck_urls_from_table(decks_table, individual_download_urls)


def log_download_links(archetype_name, download_links):
    path_to_archetype_links = os.path.join(PATH_TO_LINKS_DIR, f"{archetype_name}.txt")
    # add all the links to a textfile with the archetype's name in dir "links"
    print(os.getcwd())
    with open(path_to_archetype_links, 'w') as w:
        for link in download_links:
            w.write(link)
            w.write("\n")


def _extract_deck_urls_from_table(decks_table, individual_download_urls):
    table_rows = decks_table.find_all('tr')
    num_urls = 0
    for row in table_rows:
        if num_urls >= MAX_LISTS_PER_ARCHETYPE:
            break
        url = _get_url_from_table_row(row)
        if url:
            individual_download_urls.append(url)
            num_urls += 1
    return individual_download_urls


def _get_url_from_table_row(row):
    row_cells = row.find_all('td')
    if len(row_cells) >= 2:
        url_cell = row_cells[1]
        raw_url = url_cell.a["href"]
        if _is_deck_url(raw_url):
            return _get_formatted_url(raw_url)
    return None


def _get_formatted_url(url):
    if url.find('http') == -1:
        url = url.strip('/deck/')
        return "http://mtggoldfish.com/deck/download/" + url


def _is_deck_url(url):
    if url.find("/deck") == -1:
        return False
    else:
        return True


if __name__ == "__main__":
    main()


