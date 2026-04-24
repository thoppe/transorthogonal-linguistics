import json
import subprocess
import sys

import numpy as np

from transorthogonal_linguistics import Features
from transorthogonal_linguistics import __version__
from transorthogonal_linguistics import ensure_words_exist
from transorthogonal_linguistics import missing_words
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
    assert callable(missing_words)
    assert callable(ensure_words_exist)
    assert callable(transorthogonal_words)
    assert callable(slerp_word_path)
    assert callable(validate_word)
    assert __version__ == "0.1.0"


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


def test_missing_words_helpers_and_api_error():
    features = Features()

    assert missing_words(["boy", "not-a-real-word"], features) == ["not-a-real-word"]

    try:
        ensure_words_exist(["boy", "not-a-real-word"], features)
    except ValueError as exc:
        assert "not-a-real-word" in str(exc)
    else:
        raise AssertionError("ensure_words_exist should raise for missing vocabulary")

    try:
        transorthogonal_words("boy", "not-a-real-word", features)
    except ValueError as exc:
        assert "not-a-real-word" in str(exc)
    else:
        raise AssertionError("transorthogonal_words should raise ValueError for missing words")


def test_cli_reports_unknown_words_cleanly():
    result = subprocess.run(
        [sys.executable, "-m", "transorthogonal_linguistics.word_path", "boy", "not-a-real-word"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Unknown word(s): 'not-a-real-word'" in result.stderr


def test_cli_reports_usage_errors_cleanly():
    result = subprocess.run(
        [sys.executable, "-m", "transorthogonal_linguistics.word_path", "boy"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "expected an even number of input words" in result.stderr


def test_cli_supports_version_flag():
    result = subprocess.run(
        [sys.executable, "-m", "transorthogonal_linguistics.word_path", "--version"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert __version__ in result.stdout


def test_cli_supports_json_output():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "transorthogonal_linguistics.word_path",
            "--format",
            "json",
            "boy",
            "man",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)

    assert isinstance(payload, list)
    assert payload
    assert {"word", "distance", "time"} <= set(payload[0])
