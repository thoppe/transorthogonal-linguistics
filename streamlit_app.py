from __future__ import annotations

from collections import defaultdict

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
HOMEPAGE_URL = "https://transorthogonal-linguistics.streamlit.app/"
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


def bucket_time(time_value: float) -> int:
    if time_value >= 1.0:
        return 9
    return max(0, min(9, int(time_value * 10)))


def format_tier_range(bucket_index: int) -> str:
    start = bucket_index / 10
    if bucket_index == 9:
        return f"{start:.1f} to 1.0"
    end = (bucket_index + 1) / 10
    return f"{start:.1f} to {end:.1f}"


def tiered_result_rows(result):
    tiers = defaultdict(list)
    records = result_records(result)
    last_index = len(records) - 1
    for index, row in enumerate(records):
        time = 0.0 if abs(row["time"]) < 0.0005 else row["time"]
        bucket_index = bucket_time(float(time))
        tiers[bucket_index].append(
            {
                "word": str(row["word"]),
                "time": float(time),
                "is_first": index == 0,
                "is_last": index == last_index,
            }
        )

    return [
        {
            "index": bucket_index,
            "label": format_tier_range(bucket_index),
            "words": tiers.get(bucket_index, []),
        }
        for bucket_index in range(10)
    ]


def format_tier_words(words):
    if not words:
        return "-"
    return ", ".join(word["word"] for word in words)


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

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Mono:wght@400&family=Source+Sans+3:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: "Source Sans 3", sans-serif;
    }

    .app-title {
        font-family: "Fraunces", serif;
        font-weight: 600;
        font-size: 2.9rem;
        line-height: 0.95;
        letter-spacing: -0.02em;
        margin: 0 0 0.35rem 0;
    }

    .app-caption {
        font-family: "Source Sans 3", sans-serif;
        font-size: 1.05rem;
        max-width: 48rem;
        margin: 0 0 1.25rem 0;
        color: inherit;
        opacity: 0.8;
    }

    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] p {
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
        line-height: 1.1;
    }

    div[data-testid="stHorizontalBlock"] p {
        font-family: "IBM Plex Mono", monospace;
    }

    .tier-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 1.25rem;
    }

    .tier-card {
        border: 1px solid rgba(15, 23, 42, 0.12);
        border-radius: 18px;
        padding: 1rem 1rem 0.95rem 1rem;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.94), rgba(244,247,251,0.96));
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        min-height: 10rem;
    }

    .tier-topline {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 0.7rem;
    }

    .tier-index {
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6b7280;
    }

    .tier-range {
        font-family: "Fraunces", serif;
        font-size: 1.05rem;
        line-height: 1.1;
        color: #111827;
    }

    .tier-count {
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.78rem;
        color: #4b5563;
    }

    .tier-word-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
    }

    .tier-word {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        border-radius: 999px;
        padding: 0.38rem 0.62rem;
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.08);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.92rem;
        line-height: 1;
        color: #111827;
    }

    .tier-word-endpoint {
        width: 100%;
        justify-content: space-between;
        border-color: rgba(15, 23, 42, 0.18);
        background: linear-gradient(90deg, #ffffff, #f7fafc);
    }

    .tier-word-time {
        color: #6b7280;
        font-size: 0.8rem;
    }

    .tier-empty {
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.88rem;
        color: #9ca3af;
        padding-top: 0.15rem;
    }

    @media (max-width: 900px) {
        .tier-grid {
            grid-template-columns: minmax(0, 1fr);
        }
    }

    .tier-lines {
        font-family: "IBM Plex Mono", monospace;
        line-height: 1.7;
        font-size: 1rem;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="app-title">Transorthogonal Linguistics</div>
    <div class="app-caption">
        Explore the words that lie in between a start and end word along a semantic path
        in the bundled embedding space.
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Open the sidebar to change the start and end words.")

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
        st.link_button(":material/public: Travis", HOMEPAGE_URL, width="stretch")

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

tiers = tiered_result_rows(result)
display_lines = []
first_line = ""
final_line = ""
for tier in tiers:
    first_words = [word for word in tier["words"] if word["is_first"]]
    last_words = [word for word in tier["words"] if word["is_last"]]
    middle_words = [
        word for word in tier["words"] if not word["is_first"] and not word["is_last"]
    ]

    for first_word in first_words:
        first_line = format_tier_words([first_word])

    display_lines.append(format_tier_words(middle_words if not last_words else []))

    for last_word in last_words:
        final_line = format_tier_words([last_word])

display_lines = [first_line, *display_lines, final_line]

st.markdown(
    f'<div class="tier-lines">{"<br>".join(display_lines)}</div>',
    unsafe_allow_html=True,
)
