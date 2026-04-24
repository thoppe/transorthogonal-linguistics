__all__ = [
    "Features",
    "ensure_words_exist",
    "missing_words",
    "slerp_word_path",
    "transorthogonal_words",
    "validate_word",
]


def Features(*args, **kwargs):
    from .word_path import Features as _Features

    return _Features(*args, **kwargs)


def missing_words(*args, **kwargs):
    from .word_path import missing_words as _missing_words

    return _missing_words(*args, **kwargs)


def ensure_words_exist(*args, **kwargs):
    from .word_path import ensure_words_exist as _ensure_words_exist

    return _ensure_words_exist(*args, **kwargs)


def transorthogonal_words(*args, **kwargs):
    from .word_path import transorthogonal_words as _transorthogonal_words

    return _transorthogonal_words(*args, **kwargs)


def validate_word(*args, **kwargs):
    from .word_path import validate_word as _validate_word

    return _validate_word(*args, **kwargs)


def slerp_word_path(*args, **kwargs):
    from .slerp_word_path import slerp_word_path as _slerp_word_path

    return _slerp_word_path(*args, **kwargs)
