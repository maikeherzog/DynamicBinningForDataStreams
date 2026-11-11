import random

import numpy as np
import pytest

from clusterCreation import k_means_plus_plus, sse, calc_optimal_k, get_best_clustering, add_noise


data=[20, 22, 25, 27, 30, 89]
stream = [(1,1,20), (1,2,22), (1,3,25), (1,4,27), (1,5,30), (1,6,89)]
numOfClusters=2

def test_k_means_plus_plus():
    result = k_means_plus_plus(data, numOfClusters)
    erg = {24.8: [20, 22, 25, 27, 30], 89.0: [89]}
    assert result == erg, f"Expected {erg}, but got {result}"

def test_sse():
    clusters = {24.8: [20, 22, 25, 27, 30], 89.0: [89]}
    result = sse(clusters)
    expected_sse = 62.8
    assert result == expected_sse, f"Expected {expected_sse}, but got {result}"

def test_calc_optimal_k():
    different_k = {1: 3497.5, 2: 62.8, 3: 17.17, 4: 4, 5: 2}
    result = calc_optimal_k(different_k)
    expected_k = 2
    assert result == expected_k, f"Expected {expected_k}, but got {result}"

def test_get_best_clustering():
    result = get_best_clustering(data, numOfClusters)
    expected_histogram = {(20, 30): 5, (89, 89): 1}
    assert result == expected_histogram, f"Expected {expected_histogram}, but got {result}"

