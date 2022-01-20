import requests
from bs4 import BeautifulSoup
import os
import urllib3
import time

LIST_CAP = 40 # maximum number of lists per archetype

def get_links(current):  
    pages = [] 
    html_texts = []
    num_lists = 0 # number of lists from this archetype gathered
    
    main_html = requests.get(current, verify=False).text
    soup = BeautifulSoup(main_html, 'html.parser')
    table = soup.find('table', class_='table table-striped')
    links = table.findAll('a')
    # until frontier is empty or list cap is reached
    for i in range(LIST_CAP):
        link = links[i*3]['href'] # only every 3rd link is deck
        if link.find("/deck") != -1:
            if link.find('http') == -1:
                link = link.strip('/deck/')
                link = "http://mtggoldfish.com/deck/download/"+link
            pages.append(link)
            page_html = requests.get(link, verify=False).text
            print('page accessed! ', link)
            html_texts.append(page_html)



        num_lists += 1

    return((pages, html_texts))

def main():
    urllib3.disable_warnings()
    # name of the folder that will be created and contain the archetype of list current
    name = "HammerTime"
    current = "https://www.mtggoldfish.com/archetype/modern-hammer-time/decks" # there might be issues with the long weird name (try initial = one of the side ones) 
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
    for list_text in html_texts:
    
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