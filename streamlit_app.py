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
    st.session_state.auto_trace = True


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

with st.sidebar:
    start_word = st.text_input("Start word", key="start_word").strip()
    end_word = st.text_input("End word", key="end_word").strip()
    method_col, cutoff_col = st.columns(2)
    with method_col:
        method = st.radio("Path method", ["Straight Line", "Slerp"], index=0)
    with cutoff_col:
        word_cutoff = st.slider("Result limit", min_value=10, max_value=50, value=25, step=5)
    selected_pair = st.selectbox(
        "Quick examples",
        EXAMPLE_PAIRS,
        index=0,
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

default_start, default_end = selected_pair
st.session_state.setdefault("start_word", default_start)
st.session_state.setdefault("end_word", default_end)
st.session_state.setdefault("auto_trace", True)
st.session_state.pop("auto_trace", False)

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
