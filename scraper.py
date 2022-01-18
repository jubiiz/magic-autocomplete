import requests
from bs4 import BeautifulSoup
import os

LIST_CAP = 5 # maximum number of lists per archetype

def find_unexplored(current, explored):
    pass
    #TODO

def main():
    name = "HammerTime"
    current = "https://www.mtggoldfish.com/archetype/modern-hammer-time#paper" # there might be issues with the long weird name (try initial = one of the side ones) 

    frontier = [current]
    explored = []    
    num_lists = 0 # number of lists from this archetype gathered

    while len(frontier != 0 and num_lists < LIST_CAP):
        # exploring next list
        current = frontier.pop()
        explored.append(current)
        num_lists += 1

        # find all new links that aren't in explored
        for link in find_unexplored(current, explored):
            frontier.append(link)
        
    folder_path = os.path.join(os.getcwd(), f"unf_lists{os.sep}{name}")
    try:
        os.mkdir(folder_path)
    except Exception as E:
        print("exception: ", E)


    for link in explored:
        # UNFINISHED
        print("link: ", link)

    




if __name__ == "__main__":
    main()