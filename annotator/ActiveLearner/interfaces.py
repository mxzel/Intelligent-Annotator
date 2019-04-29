import random
import numpy as np

random.seed(0)


def calc_entropies(probs: np.array):
    entropies = -probs * np.log(probs)
    return entropies


def get_max_k_entropies_index(entropies: np.array, k: int):
    return entropies.argsort()[-k:][::-1]


def generate_next_train_set():
    pass

