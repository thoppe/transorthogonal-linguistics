import numpy as np

try:
    from . import word_path as wp
except ImportError:  # pragma: no cover - supports direct script execution
    import word_path as wp

def build_local_features(w0,w1,features,n_local):
    local_features = wp.Features(empty=True)
    vocab,_,_ = wp.transorthogonal_words(w0,w1,features,n_local)
    feat = np.vstack([features[w] for w in vocab])

    local_features.vocab = vocab
    local_features.features = feat

    local_features.reindex()
    return local_features

def slerp_points(x0,x1,slerp_n):
    ''' N-dimensional slerp interpolation '''
    theta = np.arccos(x0.dot(x1))
    st = np.sin(theta)

    T  = np.linspace(0,1,slerp_n)
    L1 = np.sin((1-T)*theta)/st
    L2 = np.sin(T*theta)/st
    SL = np.outer(L1,x0) + np.outer(L2,x1)
    
    return (SL.T / np.linalg.norm(SL,axis=1)).T

def slerp_word_path(w0,w1,features,
                    threshold_cutoff=1.1,
                    slerp_n=20,
                    n_local=5000):
    wp.ensure_words_exist((w0, w1), features)

    lf = build_local_features(w0,w1,features,n_local)

    T  = np.linspace(0,1,slerp_n)
    SL = slerp_points(lf[w0],lf[w1],slerp_n)

    GEO = []

    for t,L in zip(T,SL):
        cosine_dist   = np.dot(lf.features, L)
        cosine_dist[cosine_dist>=1] = 1.0
        geodesic_dist = np.arccos(cosine_dist)

        GEO.append(geodesic_dist)

    GEO = np.vstack(GEO)

    # Only choose words that are closer to the path than an end point, e.g.
    # ignore this situation:         (o)  (x)------(x)
    # and accept this situtation:         (x)--o---(x)
    MIN_IDX = np.argmin(GEO,axis=0)
    CONCAVE_MASK = (MIN_IDX>0) & (MIN_IDX<slerp_n-1)

    idx_concave = np.where(CONCAVE_MASK)[0]
    vocab = np.array([lf.index2word(idx) for idx in idx_concave])
    dist  = GEO[MIN_IDX[idx_concave], idx_concave]
    time  = np.array([T[idx] for idx in MIN_IDX[CONCAVE_MASK]])

    # Limit results to this many
    total_word_cut = 50

    top_idx = np.argsort(dist)
    vocab = vocab[top_idx][:total_word_cut]
    time  = time [top_idx][:total_word_cut]
    dist  = dist [top_idx][:total_word_cut]

    threshold_idx = dist<threshold_cutoff
    vocab = vocab[threshold_idx]
    time  = time [threshold_idx]
    dist  = dist [threshold_idx]    
    
    chrono_idx = np.argsort(time)
    vocab = vocab[chrono_idx]
    time  = time [chrono_idx]
    dist  = dist [chrono_idx]

    # Add back in the endpoints
    vocab = np.hstack([[w0],vocab,[w1]])
    time  = np.hstack([[0.],time, [1.]])
    dist  = np.hstack([[0.],dist, [0.]])

    return (vocab, dist, time)

def build_parser():
    import argparse

    desc = (
        "Find words near a spherical interpolation path between each pair "
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
        version=f"%(prog)s {wp.__version__}",
    )
    parser.add_argument("--f_features",
                        help="path to the NumPy feature matrix",
                        default=wp._default_feature_file)
    parser.add_argument("--f_vocab",
                        help="path to the NumPy vocabulary vector",
                        default=wp._default_vocab_file)
    parser.add_argument("--threshold_cutoff", '-c',
                        help="maximum geodesic distance for retained words",
                        type=float, default=1.05)
    parser.add_argument("--slerp_n", '-s',
                        help="number of interpolation points along the path",
                        type=int, default=25)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    parser.add_argument(
        "--log-level",
        choices=("DEBUG", "INFO", "WARNING", "ERROR"),
        help="enable logging at the selected level",
    )
    parser.add_argument("words",
                        nargs="*",
                        metavar="WORD",
                        help="space-separated word pairs, e.g. boy man mind body")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    wp.configure_logging(args.log_level)

    if not args.words:
        parser.error("expected at least one pair of input words")

    if len(args.words) % 2 != 0:
        parser.error("expected an even number of input words")

    word_pairs = [[w1, w2] for w1, w2 in zip(args.words[::2],
                                             args.words[1::2])]
    
    features = wp.Features()

    for k, (w0, w1) in enumerate(word_pairs):
        try:
            result = slerp_word_path(w0, w1, features,
                                     slerp_n=args.slerp_n,
                                     threshold_cutoff=args.threshold_cutoff)
        except ValueError as exc:
            parser.error(str(exc))

        if k and args.format == "text":
            print()

        wp.emit_result(result, args.format)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
