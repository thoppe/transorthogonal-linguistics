from __future__ import annotations

import streamlit as st

from transorthogonal_linguistics import Features
from transorthogonal_linguistics import validate_word
from transorthogonal_linguistics.slerp_word_path import slerp_word_path
from transorthogonal_linguistics.word_path import transorthogonal_words
from transorthogonal_linguistics.word_path import result_records


EXAMPLE_PAIRS = [
    ("boy", "man"),
    ("sun", "moon"),
    ("mind", "body"),
    ("good", "bad"),
    ("heaven", "hell"),
    ("war", "peace"),
]

GITHUB_URL = "https://github.com/thoppe/transorthogonal-linguistics"
HOMEPAGE_URL = "http://thoppe.github.io/"
DEFAULT_METHOD = "Slerp"
DEFAULT_WORD_CUTOFF = 25
METHOD_QUERY_VALUES = {
    "Slerp": "slerp",
    "Straight Line": "straight-line",
}
QUERY_METHOD_VALUES = {value: key for key, value in METHOD_QUERY_VALUES.items()}


@st.cache_resource(show_spinner=False)
def load_features() -> Features:
    return Features()


def result_rows(result):
    rows = []
    for row in result_records(result):
        time = 0.0 if abs(row["time"]) < 0.0005 else row["time"]
        rows.append((str(row["word"]), f"({time:.3f})"))
    return rows


def run_query(method: str, start_word: str, end_word: str, features: Features, limit: int):
    if method == "Straight Line":
        return transorthogonal_words(start_word, end_word, features, word_cutoff=limit)

    return slerp_word_path(start_word, end_word, features, slerp_n=25)


def apply_selected_example():
    start_word, end_word = st.session_state.selected_pair
    st.session_state.start_word = start_word
    st.session_state.end_word = end_word


def get_query_param(name: str, default: str = "") -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def parse_word_cutoff(value: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return DEFAULT_WORD_CUTOFF

    return min(50, max(10, parsed))


def initial_selected_pair(start_word: str, end_word: str):
    pair = (start_word, end_word)
    if pair in EXAMPLE_PAIRS:
        return pair
    return EXAMPLE_PAIRS[0]


def sync_query_params(start_word: str, end_word: str, method: str, word_cutoff: int):
    params = {}
    if start_word:
        params["start"] = start_word
    if end_word:
        params["end"] = end_word
    if method != DEFAULT_METHOD:
        params["method"] = METHOD_QUERY_VALUES[method]
    if word_cutoff != DEFAULT_WORD_CUTOFF:
        params["limit"] = str(word_cutoff)

    st.query_params.clear()
    for key, value in params.items():
        st.query_params[key] = value


st.set_page_config(
    page_title="Transorthogonal Linguistics",
    page_icon="🪐",
    layout="wide",
)

st.title("Transorthogonal Linguistics")
st.caption(
    "Explore the words that lie in between a start and end word along a semantic path in the bundled embedding space."
)
st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] p {
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
        line-height: 1.1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

query_start_word = get_query_param("start", "boy").strip()
query_end_word = get_query_param("end", "man").strip()
query_method = QUERY_METHOD_VALUES.get(get_query_param("method"), DEFAULT_METHOD)
query_word_cutoff = parse_word_cutoff(get_query_param("limit", str(DEFAULT_WORD_CUTOFF)))

st.session_state.setdefault("start_word", query_start_word)
st.session_state.setdefault("end_word", query_end_word)
st.session_state.setdefault("path_method", query_method)
st.session_state.setdefault("word_cutoff", query_word_cutoff)
st.session_state.setdefault(
    "selected_pair",
    initial_selected_pair(query_start_word, query_end_word),
)

with st.sidebar:
    start_word = st.text_input("Start word", key="start_word").strip()
    end_word = st.text_input("End word", key="end_word").strip()
    method_col, cutoff_col = st.columns(2)
    with method_col:
        method = st.radio("Path method", ["Slerp", "Straight Line"], key="path_method")
    with cutoff_col:
        word_cutoff = st.slider(
            "Result max limit",
            min_value=10,
            max_value=50,
            step=5,
            key="word_cutoff",
        )
    selected_pair = st.selectbox(
        "Quick examples",
        EXAMPLE_PAIRS,
        key="selected_pair",
        on_change=apply_selected_example,
        format_func=lambda pair: f"{pair[0]} → {pair[1]}",
    )
    st.markdown(
        "The straight-line method follows the original linear approximation. "
        "Slerp uses spherical interpolation and usually returns a tighter path."
    )
    st.divider()
    st.markdown("**Links**")
    github_col, homepage_col = st.columns(2)
    with github_col:
        st.link_button(":material/code: GitHub", GITHUB_URL, width="stretch")
    with homepage_col:
        st.link_button(":material/public: Travis Hoppe", HOMEPAGE_URL, width="stretch")

features = load_features()

sync_query_params(start_word, end_word, method, word_cutoff)

if not start_word or not end_word:
    st.info("Pick a pair from the sidebar or type your own words in the sidebar inputs.")
    st.stop()

missing = [word for word in (start_word, end_word) if not validate_word(word, features)]
if missing:
    quoted = ", ".join(repr(word) for word in missing)
    st.error(f"Unknown word(s): {quoted}")
    st.stop()

try:
    result = run_query(method, start_word, end_word, features, word_cutoff)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

for word, time_label in result_rows(result):
    word_col, time_col = st.columns([3, 1], gap="small")
    with word_col:
        st.markdown(word)
    with time_col:
        st.markdown(time_label)
