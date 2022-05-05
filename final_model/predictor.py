import os

import numpy as np
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences

from utils import decklist_from_path, cardnames_to_nums, nums_to_cardnames
from metadata import TEST_INPUTS_DIR, MODELS_DIR


def load_model(name: str = 'mymodel') -> tf.keras.models.Model:
    path_to_model = os.path.join(MODELS_DIR, name)
    return tf.keras.models.load_model(path_to_model)


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
    output_distribution = model(processed_input, False)
    output_numbers = list(tf.argmax(output_distribution, axis=2).numpy())[0]

    if verbose:
        output_names = nums_to_cardnames(output_numbers)
        print("Input data:\n\n", input_names)
        print('#'*50, "\n")
        print("Output Data:\n\n", output_names)

    return output_numbers


def main():
    test_file_path = os.path.join(TEST_INPUTS_DIR, 'test0.txt')
    input_names = decklist_from_path(test_file_path)
    model = load_model(name='mymodel')
    predict_list(input_names, model, verbose=1)
    print("Done.")


if __name__ == "__main__":
    main()
