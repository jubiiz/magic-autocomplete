import os

PATH_TO_DATA_DIR = f"{os.getcwd()}/../data_18_12_2023"
PATH_TO_UNFORMATTED_DECKLIST_DIR = os.path.join(PATH_TO_DATA_DIR, "unformatted_decklists")
PATH_TO_FORMATTED_DECKLIST_DIR = os.path.join(PATH_TO_DATA_DIR, "formatted_decklists")
PATH_TO_FORMATTED_UNIQUE_CARDNAMES = os.path.join(PATH_TO_DATA_DIR, "formatted_unique_cardnames.txt")
PATH_TO_LINKS_DIR = os.path.join(PATH_TO_DATA_DIR, "links")

PATH_TO_MODELS_DIR = f"{os.getcwd()}/../models"
PATH_TO_W2V_MODELS_DIR = f"{PATH_TO_MODELS_DIR}/w2v"
