from __future__ import absolute_import
import numpy as np


def rank_sup(image, rad):
    nl, nc = image.shape
    rank_values = np.zeros([nl, nc])
    for i in range(-rad, rad + 1):  # indice de ligne
        for j in range(-rad, rad + 1):  # indice de colonne
            if i != 0:
                if i < 0:
                    tmp = np.concatenate([image[-i:, :], np.zeros([-i, nc])], axis=0)
                else:
                    tmp = np.concatenate([np.zeros([i, nc]), image[:-i, :]], axis=0)
            else:
                tmp = image
            if j != 0:
                if j < 0:
                    tmp = np.concatenate([tmp[:, -j:], np.zeros([nl, -j])], axis=1)
                else:
                    tmp = np.concatenate([np.zeros([nl, j]), tmp[:, :-j]], axis=1)

            idx = tmp > image
            rank_values[idx] = rank_values[idx] + 1

    return rank_values


def rank_inf(image, rad):
    nl, nc = image.shape
    rank_values = np.zeros([nl, nc])
    for i in range(-rad, rad + 1):
        for j in range(-rad, rad + 1):
            if i != 0:
                if i < 0:  # on decalle vers le haut de i lignes
                    tmp = np.concatenate([image[-i:, :], np.zeros([-i, nc])], axis=0)
                else:
                    tmp = np.concatenate([np.zeros([i, nc]), image[:-i, :]], axis=0)
            else:
                tmp = image
            if j != 0:
                if j < 0:
                    tmp = np.concatenate([tmp[:, -j:], np.zeros([nl, -j])], axis=1)
                else:
                    tmp = np.concatenate([np.zeros([nl, j]), tmp[:, :-j]], axis=1)

            idx = tmp < image
            rank_values[idx] = rank_values[idx] + 1

    return rank_values
