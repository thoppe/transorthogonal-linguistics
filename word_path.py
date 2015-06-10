import logging
import numpy as np

_default_feature_file = "db/features.npy"
_default_vocab_file = "db/vocab.npy"


def validate_word(w, features):
    # Returns true if the word exists
    return w in features.inv_index


def save_features(f_features="db/features.word2vec"):
    # Helper function to convert gensim -> numpy
    import cPickle as _pickle
    with open(f_features) as FIN:
        features = _pickle.load(FIN)

    features.syn0 = np.load(f_features + ".syn0.npy")

    np.save(_default_feature_file,
            features.syn0)
    logging.info("Saved features {}".format(_default_feature_file))

    features.init_sims()
    vocab_n = len(features.vocab.keys())
    words = np.array([features.index2word[n] for n in xrange(0, vocab_n)])
    np.save(_default_vocab_file, words)

    logging.info("Saved vocab {}".format(_default_feature_file))


class Features(object):

    '''
    Helper class to simulate the numerical aspects of a gensim word2vec.
    '''

    def __init__(self,
                 f_features=_default_feature_file,
                 f_vocab=_default_vocab_file):

        msg = "Loading feature file {}".format(f_features)
        logging.warning(msg)
        self.features = np.load(f_features)

        msg = "Loading vocab file {}".format(f_vocab)
        logging.warning(msg)
        self.vocab = np.load(f_vocab)

        self.index = dict(zip(range(len(self)), self.vocab))
        self.inv_index = dict(zip(self.index.values(), self.index.keys()))

    def __len__(self):
        return len(self.vocab)

    def index2word(self, idx):
        return self.index[idx]

    def __getitem__(self, word):
        idx = self.inv_index[word]
        return self.features[idx]


def closest_approach(x1, x2, W):
    '''
    Define a line segement, L between the two input vectors x1,x2.
    Parameterize the line by t, that linearly goes from 0->1 as x1->x2.
    For each point in the matrix A, return the distance to the line d,
    and where along the line t.
    '''

    x21 = x2 - x1
    x21_norm = np.linalg.norm(x21)

    X10 = x1 - W
    X10_21 = X10.dot(x21)

    T = -X10_21 / x21_norm ** 2

    X10_norm = np.linalg.norm(X10, axis=1)

    D2 = (X10_norm * x21_norm) ** 2 - X10_21 ** 2
    D2 /= x21_norm ** 2

    # All values are positive, but some are ~ 0.000.
    # Make sure this is true before sqrt.
    D = np.sqrt(np.abs(D2))

    return D, T


def transorthogonal_words(w1, w2, features, word_cutoff=25):

    W = features.features
    x1 = features[w1]
    x2 = features[w2]

    D, T = closest_approach(x1, x2, W)

    close_idx = np.argsort(D)[:word_cutoff]
    WORDS = np.array([features.index2word(idx) for idx in close_idx])
    timeline = abs(T[close_idx])
    dist = D[close_idx]

    chrono_idx = np.argsort(timeline)

    return (WORDS[chrono_idx],
            dist[chrono_idx],
            timeline[chrono_idx])


if __name__ == "__main__":

    import argparse

    desc = '''
    transorthogonal words

    Moves across the lines spanned by the orthogonal space.
    Interesting cases: boy man mind body fate destiny
    teacher scientist girl woman conservative liberal
    hard soft religion rationalism
    '''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--f_features",
                        help="numpy feature matrix",
                        default=_default_feature_file)
    parser.add_argument("--f_vocab",
                        help="numpy vocab vector",
                        default=_default_vocab_file)
    parser.add_argument("--word_cutoff", '-c',
                        help="Number of words to select",
                        type=int, default=25)
    parser.add_argument("words",
                        nargs="*",
                        help="Space separated pairs of words example: "
                        "python word_path.py boy man mind body")

    args = parser.parse_args()

    if not args.words:
        msg = "You must either pick at least two words!"
        raise SyntaxError(msg)

    if len(args.words) % 2 != 0:
        msg = "You input an even number of words!"
        raise SyntaxError(msg)

    word_pairs = [[w1, w2] for w1, w2 in zip(args.words[::2],
                                             args.words[1::2])]

    features = Features(args.f_features,
                        args.f_vocab)

    for k, (w1, w2) in enumerate(word_pairs):

        result = transorthogonal_words(w1, w2,
                                       features,
                                       args.word_cutoff)

        for word, time, distance in zip(*result):
            print "{:0.5f} {:0.3f} {}".format(time, distance, word)

        if k:
            print
