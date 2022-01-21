import requests
from bs4 import BeautifulSoup
import os
import urllib3
import time

LIST_CAP = 40 # maximum number of lists per archetype

def find_unexplored(current, explored):
    """
    returns a list of unvisited decklist of the same archetype as the one on "page"
    """
    # find all the lists on this page
    unvisited = []
    page_html = ""
    htmls = []
    try:
        page_html = requests.get(current, verify=False).text
        time.sleep(0.5)
        print("page accessed! ", current)
        
    except requests.exceptions.MissingSchema:
        print(current)
        page_html = requests.get(current, verify=False).text
    soup = BeautifulSoup(page_html, 'html.parser')
    column_decks = soup.findAll('td', class_='column-deck')
    for row in column_decks:
        s = row.find('span', class_='deck-price-paper') # span
        l = s.find('a') # link        
        # add only the lists which have not yet been visited
        if l["href"] not in explored:
            unvisited.append(l["href"]) # append the "href" attribute of the link
            htmls.append(page_html)

    return((unvisited, htmls))

def get_links(current):
    frontier = [current]
    explored = []    
    html_texts = []
    num_lists = 0 # number of lists from this archetype gathered

    # until frontier is empty or list cap is reached
    while len(frontier) != 0 and num_lists < LIST_CAP:
        # exploring next list
        current = frontier.pop()
        explored.append(current)
        num_lists += 1

        # find all new links that aren't in explored
        links, htmls = find_unexplored(current, explored)
        for link in links:
            link, 
            if link.find("http") == -1:
                frontier.append("http://mtggoldfish.com"+link)
                # THIS DOESNT WORK: BECAUSE OF LACK OF #PAPER AT THE END??
            else:
                frontier.append(link)
        html_texts += htmls

    return((explored, html_texts))

def main():
    urllib3.disable_warnings()
    # name of the folder that will be created and contain the archetype of list current
    name = "HammerTime"
    current = "https://www.mtggoldfish.com/archetype/modern-hammer-time#paper" # there might be issues with the long weird name (try initial = one of the side ones) 
    # should try from here: https://www.mtggoldfish.com/archetype/modern-hammer-time/decks

    links, html_texts = get_links(current)
        
    lists_folder_path = os.path.join(os.getcwd(), f"unf_lists{os.sep}{name}")
    links_file_path = os.path.join(os.getcwd(), f"links{os.sep}{name}.txt")
    try:
        os.mkdir(lists_folder_path)
    except Exception as E:
        print("exception: ", E.__class__)

    # add all the links to a textfile with the name = name in folder "links"
    with open(links_file_path, 'w') as w:
        for link in links:
            w.write(link)
            w.write("\n")

    counter = 0
    for page_html in html_texts:
        # download the decklist at link; add it to a text file with name = counter
        #page_html = requests.get(link, verify=False).text
        time.sleep(0.5)
        soup = BeautifulSoup(page_html, "html.parser")
        a = soup.find('a', class_='btn btn-secondary deck-tools-btn dropdown-toggle')
        dl_link = a['href']
        if dl_link.find("download") == -1:
            print('error: no download button found for page: ', link)
        
        dl_link = "http://mtggoldfish.com" + dl_link
        list_text = requests.get(dl_link, verify=False).text
        file_path = os.path.join(lists_folder_path, str(counter)+".txt")

        with open(file_path, 'w') as w:
            for line in list_text.split('\r\n'):
                if len(line) == 0:
                    break
                w.write(line)
                w.write("\n")
        counter += 1
    




if __name__ == "__main__":
    main()