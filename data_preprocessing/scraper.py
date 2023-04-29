import os
import urllib3
import requests
from bs4 import BeautifulSoup

MAX_LISTS_PER_ARCHETYPE = 10

class Scraper:
    def __init__(self):
        pass

    def get_download_links_for_one_archetype(self, archetype_name, url_to_decks_page):
        individual_download_urls = []
        decks_page_html = requests.get(url_to_decks_page).text
        soup_decks_page_html = BeautifulSoup(decks_page_html, 'html.parser')
        decks_table = soup_decks_page_html.find('table', class_='table table-striped')
        table_rows = decks_table.find_all('tr')

        for i in range(MAX_LISTS_PER_ARCHETYPE):
            row = table_rows[i]
            row_data_cells = row.find_all('td')
            if len(row_data_cells) >= 2:
                url_cell = row_data_cells[1]
                raw_link = url_cell.a["href"]
                if _is_decklink(raw_link):
                    individual_download_urls.append(_get_formatted_link(raw_link))
        return individual_download_urls


def _get_formatted_link(link):
    if link.find('http') == -1:
        link = link.strip('/deck/')
        return "http://mtggoldfish.com/deck/download/" + link


def _is_decklink(link):
    if link.find("/deck") == -1:
        return False
    else:
        return True


def main():
    # name of the folder that will be created and contain the archetype of list current
    name = "MonoUTron"
    current = "https://www.mtggoldfish.com/archetype/mono-blue-tron/decks" # there might be issues with the long weird name (try initial = one of the side ones)
    #https://www.mtggoldfish.com/archetype/modern-murktide-regent/decks
    #https://www.mtggoldfish.com/archetype/modern-murktide-regent#paper

    scraper = Scraper()
    print(scraper.get_links_for_one_archetype("MonoUTron", "https://www.mtggoldfish.com/archetype/mono-blue-tron/decks"))


if __name__ == "__main__":
    main()


