import os
import time
from typing import List

import requests
from bs4 import BeautifulSoup

MAX_LISTS_PER_ARCHETYPE = 100

PATH_TO_DATA_DIR = f"{os.getcwd()}/../data_18_12_2023"
PATH_TO_UNFORMATTED_DECKLIST_DIR = os.path.join(PATH_TO_DATA_DIR, "unformatted_decklists")
PATH_TO_LINKS_DIR = os.path.join(PATH_TO_DATA_DIR, "links")

ARCHETYPES_TO_DOWNLOAD = {
    "crashing_footfalls": "https://www.mtggoldfish.com/archetype/modern-crashing-footfalls/decks",
    "yawgmoth": "https://www.mtggoldfish.com/archetype/modern-yawgmoth-9bd3dc9a-1da1-442e-9b88-6ef2a027e80b/decks",
    "amulet_titan": "https://www.mtggoldfish.com/archetype/amulet-titan/decks",
    "murktide_regent": "https://www.mtggoldfish.com/archetype/modern-murktide-regent/decks",
    "mono_green_tron": "https://www.mtggoldfish.com/archetype/modern-mono-green-tron/decks",
    "hammer_time": "https://www.mtggoldfish.com/archetype/modern-hammer-time/decks",
    "living_end": "https://www.mtggoldfish.com/archetype/modern-living-end/decks",
    "boros_burn": "https://www.mtggoldfish.com/archetype/modern-boros-burn/decks",
    "hardened_scales": "https://www.mtggoldfish.com/archetype/g/decks",
    "mono_black_coffers": "https://www.mtggoldfish.com/archetype/modern-mono-black-coffers/decks",
    "indomitable_creativity": "https://www.mtggoldfish.com/archetype/modern-indomitable-creativity/decks",
    "deaths_shadow": "https://www.mtggoldfish.com/archetype/modern-death-s-shadow-472/decks",
    "domain_zoo": "https://www.mtggoldfish.com/archetype/modern-domain-zoo/decks",
    "grixis_control": "https://www.mtggoldfish.com/archetype/modern-grixis-control/decks",
    "merfolk": "https://www.mtggoldfish.com/archetype/merfolk/decks",
    "mill": "https://www.mtggoldfish.com/archetype/modern-mill/decks",
    "4c_omnath": "https://www.mtggoldfish.com/archetype/modern-4-5c-omnath/decks",
    "goryos_vengence": "https://www.mtggoldfish.com/archetype/modern-goryo-s-vengeance/decks",
    "jund_saga": "https://www.mtggoldfish.com/archetype/modern-jund-saga/decks",
    "jeskai_controll": "https://www.mtggoldfish.com/archetype/jeskai-control-42a2c2ee-6eb3-4db1-8da6-eaec7077a1e0/decks",
    "red_blue_control": "https://www.mtggoldfish.com/archetype/blue-red-control/decks",
    "azorius_control": "https://www.mtggoldfish.com/archetype/wu-68d6e340-6601-4aab-9a70-4bdccc013e7e/decks",
    "humans": "https://www.mtggoldfish.com/archetype/humans-f09079c9-02d4-48b2-9774-994fc95bc2c9/decks",
    "dimir_control": "https://www.mtggoldfish.com/archetype/modern-dimir-control/decks",
    "thopter_combo": "https://www.mtggoldfish.com/archetype/modern-thopter-combo/decks",
    "twiddle_storm": "https://www.mtggoldfish.com/archetype/modern-twiddle-storm/decks",
    "infect": "https://www.mtggoldfish.com/archetype/infect/decks",
    "grinding_station": "https://www.mtggoldfish.com/archetype/modern-grinding-station/decks",
    "mono_blue_tron": "https://www.mtggoldfish.com/archetype/mono-blue-tron/decks",
    "eldrazi_tron": "https://www.mtggoldfish.com/archetype/eldrazi-tron/decks",
    "prison_tron": "https://www.mtggoldfish.com/archetype/modern-prison-tron/decks",
}


def main():
    """
    Scrape as many lists as possible per archetype and store them in a text file
    """
    for archetype_name, url_to_deck_page in ARCHETYPES_TO_DOWNLOAD.items():
        print(archetype_name, url_to_deck_page)
        try:
            scrape_lists_for_archetype(archetype_name, url_to_deck_page)
        except Exception as e:
            print(f"Failed to scrape for archetype: {archetype_name}")


def scrape_lists_for_archetype(archetype_name: str, url_to_deck_page: str) -> None:
    download_links = get_download_urls_for_one_archetype(url_to_deck_page)
    write_download_links(archetype_name, download_links)
    write_lists_for_archetype(archetype_name, download_links)


def write_lists_for_archetype(archetype_name: str, download_links: List[str]) -> None:
    """
    downloads a decklist for each download link and writes it locally to a text file
    """
    counter = 0
    path_to_unformatted_decklists_dir_for_archetype = os.path.join(PATH_TO_UNFORMATTED_DECKLIST_DIR, archetype_name)
    ensure_directory_is_empty(path_to_unformatted_decklists_dir_for_archetype)

    for download_link in download_links:
        try:
            time.sleep(1)  # avoids overloading the server
            decklist = get_unformatted_decklist_from_download_link(download_link)
            decklist_filename = f"{counter}.txt"
            path_to_decklist = os.path.join(path_to_unformatted_decklists_dir_for_archetype, decklist_filename)
            with open(path_to_decklist, 'w') as w:
                print(decklist, file=w, end='')
            counter += 1
        except Exception as e:
            print(f"Error: failed to parse list from decklist: {download_link}")
    print(f"Done archetype {archetype_name}, wrote {counter} decklists")


def get_unformatted_decklist_from_download_link(download_link: str) -> str:
    """
    Downloads a decklist from the download link
    """
    response = requests.get(download_link)
    text_decklist = response.text.rstrip("\r\n")
    return text_decklist


def ensure_directory_is_empty(directory: str) -> None:
    if os.path.exists(directory):
        if dir_contains_files(directory):
            raise RuntimeError(f"Directory {directory} already exists and contains data")
    else:
        os.makedirs(directory)


def get_download_urls_for_one_archetype(url_to_decks_page: str) -> List[str]:
    """
    Returns a list of all the download URLs. Each allows to download one text decklist.
    """
    decks_page_html = requests.get(url_to_decks_page).text
    decks_page_soup = BeautifulSoup(decks_page_html, 'html.parser')
    decks_table = decks_page_soup.find('table', class_='table table-striped')
    return extract_deck_download_links_from_table(decks_table)


def write_download_links(archetype_name: str, download_links: List[str]) -> None:
    """
    Writes all the download links for this archetype to a text file
    """
    path_to_archetype_links = os.path.join(PATH_TO_LINKS_DIR, f"{archetype_name}.txt")
    # add all the links to a textfile with the archetype's name in dir "links"
    with open(path_to_archetype_links, 'w') as w:
        for link in download_links:
            w.write(link)
            w.write("\n")


def extract_deck_download_links_from_table(decks_table: BeautifulSoup) -> List[str]:
    """
    Returns a list of download links for decklists from the html table
    """
    individual_download_urls = []
    table_rows = decks_table.find_all('tr')
    num_urls = 0
    for row in table_rows:
        if num_urls >= MAX_LISTS_PER_ARCHETYPE:
            break
        url = get_deck_download_link_from_table_row(row)
        if url:
            individual_download_urls.append(url)
            num_urls += 1
    return individual_download_urls


def get_deck_download_link_from_table_row(row):
    row_cells = row.find_all('td')
    if len(row_cells) >= 2:
        url_cell = row_cells[1]
        raw_url = url_cell.a["href"]
        if is_a_download_link(raw_url):
            return get_formatted_download_link(raw_url)


def get_formatted_download_link(url: str) -> str:
    if url.find('http') == -1:
        url = url.strip('/deck/')
        return "http://mtggoldfish.com/deck/download/" + url


def is_a_download_link(url: str) -> bool:
    if url.find("/deck") == -1:
        return False
    else:
        return True


def dir_contains_files(directory: str) -> bool:
    return len(os.listdir(directory)) != 0


if __name__ == "__main__":
    main()


