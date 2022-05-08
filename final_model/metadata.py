"""
Here is stored the final model's metadata, such as data paths
There are 800 decklists
There are 578 single cards
len(F_SINGLES) = 579 because padding_cardname
# TODO: ADD PERSONNAL ACCESS TOKEN TO GITHUB, this is a modification
"""
import os

VOCAB_SIZE = 579 # because of the extra 1 card
# WARNING: HARDCODED FOR THE SPECIFIC DATASET USED FOR THIS PROJECT

ROOT_DIR = '/home/julien/coding/PIMA/magic-autocomplete/'
CURRENT_DIR = os.path.join(ROOT_DIR, 'final_model')

DATA_DIR = os.path.join(ROOT_DIR, 'data')
TEST_INPUTS_DIR = os.path.join(CURRENT_DIR, 'test_inputs')
F_SINGLES_PATH = os.path.join(DATA_DIR, 'f_singles.txt')
UNF_SINGLES_PATH = os.path.join(DATA_DIR, 'unf_singles.txt')
F_LISTS_DIR = os.path.join(DATA_DIR, 'f_lists')
UNF_LISTS_DIR = os.path.join(DATA_DIR, 'unf_lists')

AUG_INDEXES = list(range(1, 60, 3))

MODELS_DIR = os.path.join(CURRENT_DIR, 'model')


