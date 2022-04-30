from metadata import F_SINGLES_PATH, UNF_SINGLES_PATH, F_LISTS_DIR, UNF_LISTS_DIR
from utils import load_decklists, train_test_val_split, get_aug_inputs_and_labels
# from model import build_model

def run():
    decklists = load_decklists()
    raw_train, raw_test, raw_val = train_test_val_split(decklists)

    aug_train_inputs, aug_train_labels = get_aug_inputs_and_labels(raw_train)
    aug_test_inputs, aug_test_labels = get_aug_inputs_and_labels(raw_test)
    aug_val_inputs, aug_val_labels = get_aug_inputs_and_labels(raw_val)

    # model = build_model()



if __name__ == "__main__":
    run()
