import os
import urllib3
import requests
from bs4 import BeautifulSoup

MAX_LISTS_PER_ARCHETYPE = 50


class Scraper:
    def __init__(self):
        pass

    def get_download_urls_for_one_archetype(self, url_to_decks_page):
        individual_download_urls = []
        decks_page_html = requests.get(url_to_decks_page).text
        decks_page_soup = BeautifulSoup(decks_page_html, 'html.parser')
        decks_table = decks_page_soup.find('table', class_='table table-striped')
        return self._extract_deck_urls_from_table(decks_table, individual_download_urls)

    def _extract_deck_urls_from_table(self, decks_table, individual_download_urls):
        table_rows = decks_table.find_all('tr')
        num_urls = 0
        for row in table_rows:
            if num_urls >= MAX_LISTS_PER_ARCHETYPE:
                break
            url = self._get_url_from_table_row(row)
            if url:
                individual_download_urls.append(url)
                num_urls += 1
        return individual_download_urls

    def _get_url_from_table_row(self, row):
        row_cells = row.find_all('td')
        if len(row_cells) >= 2:
            url_cell = row_cells[1]
            raw_url = url_cell.a["href"]
            if self._is_deck_url(raw_url):
                return self._get_formatted_url(raw_url)
        return None

    def _get_formatted_url(self, url):
        if url.find('http') == -1:
            url = url.strip('/deck/')
            return "http://mtggoldfish.com/deck/download/" + url

    def _is_deck_url(self, url):
        if url.find("/deck") == -1:
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
    print(scraper.get_download_urls_for_one_archetype("https://www.mtggoldfish.com/archetype/mono-blue-tron/decks"))


if __name__ == "__main__":
    main()


