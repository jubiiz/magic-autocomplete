"""
Here is stored the final model's metadata, such as data paths
There are 800 decklists
There are 578 single cards
len(F_SINGLES) = 579 because padding_cardname
"""
import os

ROOT_DIR = 'U:\documents\loisirs\programmation\PI-MA\magic-autocomplete'  # get out of the three packages
CURRENT_DIR = os.path.join(ROOT_DIR, 'final_model')

DATA_DIR = os.path.join(ROOT_DIR, 'data')
F_LISTS_DIR = os.path.join(DATA_DIR, 'f_lists')
F_SINGLES_PATH = os.path.join(DATA_DIR, 'f_singles.txt')
UNF_LISTS_DIR = os.path.join(DATA_DIR, 'unf_lists')
UNF_SINGLES_PATH = os.path.join(DATA_DIR, 'unf_singles.txt')
TEST_INPUTS_DIR = os.path.join(CURRENT_DIR, 'test_inputs')

VOCAB_SIZE = 579  # because of the extra 1 card
# WARNING: HARDCODED FOR THE SPECIFIC DATASET USED FOR THIS PROJECT
AUG_INDEXES = list(range(1, 60, 3))
MODELS_DIR = os.path.join(CURRENT_DIR, 'model')

BUCKET_NAME = "magic-autocomplete"
BUCKET_DATA_PREFIX = 'data/f_lists'
PROJECT_NAME = "storied-box-346921"
