"""
Here is stored the final model's metadata, such as data paths
There are 800 decklists
There are 578 single cards
len(F_SINGLES) = 579 because padding_cardname
# TODO: ADD PERSONNAL ACCESS TOKEN TO GITHUB, this is a modification
"""
import os

ROOT_DIR = '/home/julien/coding/PIMA/magic-autocomplete/'
CURRENT_DIR = os.path.join(ROOT_DIR, 'final_model')

DATA_DIR = os.path.join(ROOT_DIR, 'data')
F_SINGLES_PATH = os.path.join(DATA_DIR, 'f_singles.txt')
UNF_SINGLES_PATH = os.path.join(DATA_DIR, 'unf_singles.txt')
F_LISTS_DIR = os.path.join(DATA_DIR, 'f_lists')
UNF_LISTS_DIR = os.path.join(DATA_DIR, 'unf_lists')

AUG_INDEXES = list(range(1, 60))
