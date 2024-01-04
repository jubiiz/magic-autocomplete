import os

import numpy as np
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences

from main_package.scripts.metadata import TEST_INPUTS_DIR, MODELS_DIR
from main_package.scripts.utils import decklist_from_path, card_names_to_nums, nums_to_cardnames, quantities_to_cardnums
from main_package.scripts.model import MatchingPairsPercent


def _predict_list_from_numbers(padded_list: np.ndarray, model) -> np.ndarray:
    """
    takes in test_inputs (list of cardnames) and model (callable model)
    model must return a prediction as a list of numbers
    if verbose > 0, display prediction info accordingly
    Returns a list of numbers (card indexes)
    """
    output_quantities = model(padded_list, False)[0].numpy()
    output_cardnums = quantities_to_cardnums(output_quantities)
    return output_cardnums


def _load_model(name: str = 'best_3') -> tf.keras.models.Model:
    path_to_model = os.path.join(MODELS_DIR, name)
    print(path_to_model)
    return tf.keras.models.load_model(path_to_model, custom_objects=MatchingPairsPercent)


def _get_number_list_from_path(test_file_path: str):
    decklist = decklist_from_path(test_file_path)
    card_numbers = card_names_to_nums(decklist)
    return card_numbers


def _process_number_list(num_inputs: list) -> np.ndarray:
    processed_inputs = pad_sequences([num_inputs], maxlen=59, padding='pre', dtype=np.float32)
    return tf.constant(processed_inputs, name='inputs')


def _predict_decklist_from_file(model: tf.keras.models.Model, filename: str):
    test_file_path = os.path.join(TEST_INPUTS_DIR, filename)
    card_numbers = _get_number_list_from_path(test_file_path)
    padded_card_numbers = _process_number_list(card_numbers)
    predicted_numbers = _predict_list_from_numbers(padded_card_numbers, model)
    _display_prediction(card_numbers, predicted_numbers)


def _display_prediction(input_card_numbers, prediction):
    prediction_names = nums_to_cardnames(prediction)
    input_names = nums_to_cardnames(input_card_numbers)
    print("Input data:\n\n", *input_names, sep='\n')
    print('#' * 50, "\n")
    print("Output Data:\n\n", *prediction_names, sep='\n')


def main():
    model = _load_model('best_19')
    _predict_decklist_from_file(model=model, filename='test0.txt')
    print("Done.")


if __name__ == "__main__":
    main()
