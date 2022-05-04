from metadata import F_SINGLES_PATH, UNF_SINGLES_PATH, F_LISTS_DIR, UNF_LISTS_DIR
import numpy as np
import tensorflow as tf
from utils import load_decklists, train_test_val_split, get_aug_inputs_and_labels, TrainTestValData
from model import FullARModel, compile_and_fit


def run():
    decklists = load_decklists()
    raw_train, raw_test, raw_val = train_test_val_split(decklists)

    all_data = TrainTestValData(
        train=get_aug_inputs_and_labels(raw_train),
        test=get_aug_inputs_and_labels(raw_test),
        val=get_aug_inputs_and_labels(raw_val))

    model = FullARModel()
    history = compile_and_fit(model, all_data)
    model.summary()

    tf.keras.models.save_model(model, 'model/mymodel')
    print("saved")








if __name__ == "__main__":
    tf.config.run_functions_eagerly(True)
    run()
