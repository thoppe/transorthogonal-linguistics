import json
import logging
from pathlib import Path

import numpy as np

try:
    from . import __version__
except ImportError:  # pragma: no cover - supports direct script execution
    __version__ = "0.1.0"

_MODULE_ROOT = Path(__file__).resolve().parent
_default_feature_file = str(_MODULE_ROOT / "data" / "features.npy")
_default_vocab_file = str(_MODULE_ROOT / "data" / "vocab.npy")


def validate_word(w, features):
    # Returns true if the word exists
    return w in features.inv_index


def missing_words(words, features):
    return [word for word in words if not validate_word(word, features)]


def ensure_words_exist(words, features):
    missing = missing_words(words, features)
    if missing:
        quoted = ", ".join(repr(word) for word in missing)
        raise ValueError(f"Unknown word(s): {quoted}")


def save_features(f_features="db/features.word2vec"):
    # Helper function to convert gensim -> numpy
    import pickle as _pickle
    with open(f_features, "rb") as FIN:
        features = _pickle.load(FIN)

    features.syn0 = np.load(f_features + ".syn0.npy")

    np.save(_default_feature_file,
            features.syn0)
    logging.info("Saved features {}".format(_default_feature_file))

    features.init_sims()
    vocab_n = len(features.vocab.keys())
    words = np.array([features.index2word[n] for n in range(0, vocab_n)])
    np.save(_default_vocab_file, words)

    logging.info("Saved vocab {}".format(_default_feature_file))


class Features(object):

    '''
    Helper class to simulate the numerical aspects of a gensim word2vec.
    '''

    def __init__(self,
                 f_features=_default_feature_file,
                 f_vocab=_default_vocab_file,
                 empty=False):

        if empty:
            return None

        msg = "Loading feature file {}".format(f_features)
        logging.warning(msg)
        self.features = np.load(f_features)

        msg = "Loading vocab file {}".format(f_vocab)
        logging.warning(msg)
        self.vocab = np.load(f_vocab)

        self.reindex()

    def reindex(self):
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
    ensure_words_exist((w1, w2), features)

    W = features.features
    x1 = features[w1]
    x2 = features[w2]

    D, T = closest_approach(x1, x2, W)

    close_idx = np.argsort(D)[:word_cutoff]
    vocab = np.array([features.index2word(idx) for idx in close_idx])
    time = T[close_idx]
    dist = D[close_idx]
    
    # Fix occasional rounding error
    time[time<0] = 0
    dist[dist<0] = 0

    chrono_idx = np.argsort(time)

    return (vocab[chrono_idx],
            dist[chrono_idx],
            time[chrono_idx])


def print_result(result):
    for word, time, distance in zip(*result):
        print("{:0.5f} {:0.3f} {}".format(time, distance, word))


def result_records(result):
    vocab, dist, time = result
    return [
        {
            "word": str(word),
            "distance": float(distance),
            "time": float(t),
        }
        for word, distance, t in zip(vocab, dist, time)
    ]


def emit_result(result, output_format):
    if output_format == "json":
        print(json.dumps(result_records(result)))
        return

    print_result(result)


def build_parser():
    import argparse

    desc = (
        "Find words near the straight transorthogonal path between each pair "
        "of input words."
    )
    epilog = (
        "Examples: boy man | mind body | fate destiny | "
        "teacher scientist"
    )
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument("--f_features",
                        help="path to the NumPy feature matrix",
                        default=_default_feature_file)
    parser.add_argument("--f_vocab",
                        help="path to the NumPy vocabulary vector",
                        default=_default_vocab_file)
    parser.add_argument("--word_cutoff", '-c',
                        help="maximum number of nearby words to return per pair",
                        type=int, default=25)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    parser.add_argument("words",
                        nargs="*",
                        metavar="WORD",
                        help="space-separated word pairs, e.g. boy man mind body")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.words:
        parser.error("expected at least one pair of input words")

    if len(args.words) % 2 != 0:
        parser.error("expected an even number of input words")

    word_pairs = [[w1, w2] for w1, w2 in zip(args.words[::2],
                                             args.words[1::2])]

    features = Features(args.f_features,
                        args.f_vocab)

    for k, (w1, w2) in enumerate(word_pairs):
        try:
            result = transorthogonal_words(w1, w2,
                                           features,
                                           args.word_cutoff)
        except ValueError as exc:
            parser.error(str(exc))

        if k and args.format == "text":
            print()

        emit_result(result, args.format)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
