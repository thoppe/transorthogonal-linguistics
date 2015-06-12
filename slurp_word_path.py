import collections
import numpy as np
#import pandas as pd

import word_path as wp
features = wp.Features()

def build_local_features(w0,w1,features,n_local=100):

    local_features = wp.Features(empty=True)
    vocab,_,_ = wp.transorthogonal_words(w0,w1,features,n_local)
    feat = np.vstack([features[w] for w in vocab])

    local_features.vocab = vocab
    local_features.features = feat

    local_features.reindex()
    return local_features

def slerp_points(x0,x1,slurp_n):
    ''' N-dimensional slerp interpolation '''
    theta = np.arccos(x0.dot(x1))
    st = np.sin(theta)

    T  = np.linspace(0,1,slurp_n)
    L1 = np.sin((1-T)*theta)/st
    L2 = np.sin(T*theta)/st
    SL = np.outer(L1,x0) + np.outer(L2,x1)
    
    return (SL.T / np.linalg.norm(SL,axis=1)).T

def slerp_word_path(w0,w1,feat,slurp_n=20, cutoff=35):

    T  = np.linspace(0,1,slurp_n)
    SL = slerp_points(feat[w0],feat[w1],slurp_n)

    GEO = []

    for t,L in zip(T,SL):
        cosine_dist   = np.dot(feat.features, L)
        cosine_dist[cosine_dist>=1] = 1.0
        geodesic_dist = np.arccos(cosine_dist)

        GEO.append(geodesic_dist)

    GEO = np.vstack(GEO)

    # Only choose words that are closer to the path than an end point, e.g.
    # ignore this situation:         (o)  (x)------(x)
    # and accept this situtation:         (x)--o---(x)
    MIN_IDX = np.argmin(GEO,axis=0)
    CONCAVE_MASK = (MIN_IDX>0) & (MIN_IDX<slurp_n-1)

    idx_concave = np.where(CONCAVE_MASK)[0]
    vocab = np.array([feat.index2word(idx) for idx in idx_concave])
    dist  = geodesic_dist[CONCAVE_MASK]
    time  = np.array([T[idx] for idx in MIN_IDX[CONCAVE_MASK]])

    top_idx = np.argsort(dist)[:cutoff]
    vocab = vocab[top_idx]
    time  = time [top_idx]
    dist  = dist [top_idx]

    order_idx = np.argsort(time)
    vocab = vocab[order_idx]
    time  = time [order_idx]
    dist  = dist [order_idx]

    

    print vocab, dist, time
    exit()

    return SL, vocab, dist, time

#w1,w2 = "run","walk"
#w1,w2="teacher","scientist"
#w1,w2="fate","destiny"
w1,w2 = "boy","man"

lf = build_local_features(w1,w2,features, n_local=3000)
SL,WL = slerp_word_path(w1,w2,lf)
exit()
#df = refine_top_words(SL,WL)

for word in df.index:

    time = df["t"][word]
    distance = df["dist"][word]

    if distance < 1.1:
        print "{:0.5f} {:0.3f} {}".format(time, distance, word)

