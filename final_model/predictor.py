import os

import numpy as np
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences

from main_package.scripts.metadata import TEST_INPUTS_DIR, MODELS_DIR
from main_package.scripts.utils import decklist_from_path, cardnames_to_nums, nums_to_cardnames, quantities_to_cardnums
from main_package.scripts.model import MatchingPairsPercent


def process_num_inputs(num_inputs):
    processed_inputs = pad_sequences([num_inputs], maxlen=59, padding='pre', dtype=np.float32)
    return tf.constant(processed_inputs, name='inputs')


def predict_list(input_names: list, model, verbose: int = 0) -> list:
    """
    takes in test_inputs (list of cardnames) and model (callable model)
    model must return a prediction as a list of numbers
    if verbose > 0, display prediction info accordingly
    Returns a list of numbers (card indexes)
    """
    num_inputs = cardnames_to_nums(input_names)
    processed_input = process_num_inputs(num_inputs)
    output_quantities = model(processed_input, False)[0].numpy()
    output_cardnums = quantities_to_cardnums(output_quantities)

    if verbose:
        output_names = nums_to_cardnames(output_cardnums)
        print("Input data:\n\n", *input_names, sep='\n')
        print('#'*50, "\n")
        print("Output Data:\n\n", *output_names, sep='\n')

    return output_cardnums


def load_model(name: str = 'best_3') -> tf.keras.models.Model:
    path_to_model = os.path.join(MODELS_DIR, name)
    print(path_to_model)
    return tf.keras.models.load_model(path_to_model, custom_objects={'MatchingPairsPercent': MatchingPairsPercent})


def main():
    test_file_path = os.path.join(TEST_INPUTS_DIR, 'test0.txt')
    input_names = decklist_from_path(test_file_path)
    model = load_model('best_19')
    predict_list(input_names, model, verbose=1)
    print("Done.")


if __name__ == "__main__":
    main()
