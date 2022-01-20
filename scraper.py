import requests
from bs4 import BeautifulSoup
import os
import urllib3

LIST_CAP = 3 # maximum number of lists per archetype

def find_unexplored(current, explored):
    """
    returns a list of unvisited decklist of the same archetype as the one on "page"
    """
    # find all the lists on this page
    unvisited = []
    page_html = ""
    try:
        page_html = requests.get(current, verify=False).text
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

    return(unvisited)

def get_links(current):
    frontier = [current]
    explored = []    
    num_lists = 0 # number of lists from this archetype gathered

    # until frontier is empty or list cap is reached
    while len(frontier) != 0 and num_lists < LIST_CAP:
        # exploring next list
        current = frontier.pop()
        explored.append(current)
        num_lists += 1

        # find all new links that aren't in explored
        for link in find_unexplored(current, explored):
            if link.find("http") == -1:
                frontier.append("http://mtggoldfish.com"+link)
            else:
                frontier.append(link)

def main():
    urllib3.disable_warnings()
    # name of the folder that will be created and contain the archetype of list current
    name = "HammerTime"
    current = "https://www.mtggoldfish.com/archetype/modern-hammer-time#paper" # there might be issues with the long weird name (try initial = one of the side ones) 

    links = get_links(current)
        
    lists_folder_path = os.path.join(os.getcwd(), f"unf_lists{os.sep}{name}")
    links_file_path = os.path.join(os.getcwd(), f"unf_lists{os.sep}links{os.sep}{name}.txt")
    try:
        os.mkdir(lists_folder_path)
    except Exception as E:
        print("exception: ", E.__class__)

    # add all the links to a textfile with the name = name in folder "links"
    # TODO

    counter = 0
    for link in links:
        # download the decklist at link; add it to a text file with name = counter
        file_path = os.path.join(lists_folder_path, str)

        counter += 1
    




if __name__ == "__main__":
    main()