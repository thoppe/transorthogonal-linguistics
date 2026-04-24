import subprocess
import sys

import numpy as np

from transorthogonal_linguistics import Features
from transorthogonal_linguistics import slerp_word_path
from transorthogonal_linguistics import transorthogonal_words
from transorthogonal_linguistics import validate_word


REPRESENTATIVE_WORD_PAIRS = [
    ("boy", "man"),
    ("mind", "body"),
    ("sun", "moon"),
]

REPO_ROOT = "/home/travis/git-repo/transorthogonal-linguistics"


def test_features_load_and_align():
    features = Features()

    assert features.features.ndim == 2
    assert features.vocab.ndim == 1
    assert len(features) == features.features.shape[0] == features.vocab.shape[0]


def test_known_words_exist():
    features = Features()

    for word in {"boy", "man", "mind", "body", "sun", "moon"}:
        assert validate_word(word, features)


def test_package_exports_are_available():
    assert callable(Features)
    assert callable(transorthogonal_words)
    assert callable(slerp_word_path)
    assert callable(validate_word)


def test_transorthogonal_words_returns_sorted_aligned_arrays():
    features = Features()

    for w1, w2 in REPRESENTATIVE_WORD_PAIRS:
        vocab, dist, time = transorthogonal_words(w1, w2, features, word_cutoff=25)

        assert len(vocab) == len(dist) == len(time)
        assert len(vocab) > 0
        assert np.all(np.diff(time) >= 0)
        assert np.all(dist >= 0)


def test_slerp_word_path_includes_endpoints_and_sorted_time():
    features = Features()

    for w1, w2 in REPRESENTATIVE_WORD_PAIRS:
        vocab, dist, time = slerp_word_path(w1, w2, features, slerp_n=25)

        assert len(vocab) == len(dist) == len(time)
        assert len(vocab) >= 2
        assert vocab[0] == w1
        assert vocab[-1] == w2
        assert time[0] == 0.0
        assert time[-1] == 1.0
        assert dist[0] == 0.0
        assert dist[-1] == 0.0
        assert np.all(np.diff(time) >= 0)
        assert np.all(dist >= 0)


def test_module_entrypoint_runs_without_runtime_warning():
    result = subprocess.run(
        [sys.executable, "-m", "transorthogonal_linguistics.word_path", "boy", "man"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "RuntimeWarning" not in result.stderr
    assert "boy" in result.stdout
    assert "man" in result.stdout
