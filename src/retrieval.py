import numpy as np
from itertools import islice

from sklearn.metrics.pairwise import euclidean_distances

import load
import vocabulary
from histograms import compute_histogram_database, compute_histogram


def candidates_by_histograms(im, mask, histogram_database, vocabulary):
    query_histogram = compute_histogram(im, mask, vocabulary)
    dists = euclidean_distances(query_histogram, histogram_database)
    return islice(dists[0].argsort(), 0, 200)


if __name__ == "__main__":
    from sklearn.externals.joblib import Memory
    mem = Memory(cachedir='.')

    cluster_centers = mem.cache(vocabulary.compute_vocabulary)(max_im=5)
    cluster_centers.dump('./data/vocabulary.mat')
    vocabulary = np.load('./data/vocabulary.mat')

    histogram_database = mem.cache(compute_histogram_database)(vocabulary,
                                                               max_im=5)

    gen = load.load_data()
    im, mask = gen.next()

    candidates = candidates_by_histograms(im,
                                          mask,
                                          histogram_database,
                                          vocabulary)

    print('asd')
