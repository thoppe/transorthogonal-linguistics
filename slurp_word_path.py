import collections
import numpy as np
import pandas as pd

import word_path as wp
features = wp.Features()

def build_local_features(w1,w2,features,
                         n_local=10):

    local_features = wp.Features(empty=True)
    vocab,_,_ = wp.transorthogonal_words(w1,w2,features,n_local)
    feat = np.vstack([features[w] for w in vocab])

    local_features.vocab = vocab
    local_features.features = feat

    local_features.reindex()
    return local_features

def slerp_points(wa,wb,feat,slurp_n):
    ''' N-dimensional slerp interpolation '''
    va = feat[wa]
    vb = feat[wb]

    theta = np.arccos(va.dot(vb))
    st = np.sin(theta)

    T  = np.linspace(0,1,slurp_n)
    L1 = np.sin((1-T)*theta)/st
    L2 = np.sin(T*theta)/st
    SL = np.outer(L1,va) + np.outer(L2,vb)
    
    return (SL.T / np.linalg.norm(SL,axis=1)).T

def slerp_word_path(w0,w1,feat,slurp_n=20):

    T  = np.linspace(0,1,slurp_n)
    SL = slerp_points(w0,w1,feat,slurp_n)
    WL = collections.defaultdict(dict)

    GEO = []

    for t,L in zip(T,SL):
        cosine_dist   = np.dot(feat.features, L)
        cosine_dist[cosine_dist>=1] = 1.0
        geodesic_dist = np.arccos(cosine_dist)

        GEO.append(geodesic_dist)

    GEO = np.vstack(GEO)
    
    print GEO.shape

    # Only choose words that are closer to the path than an end point, e.g.
    # ignore this situation:         (o)  (x)------(x)
    # and accept this situtation:         (x)--o---(x)
    MIN_IDX = np.argmin(GEO,axis=0)
    CONCAVE_MASK = (MIN_IDX>0) & (MIN_IDX<slurp_n-1)

    idx_concave = np.where(CONCAVE_MASK)[0]
    vocab = [feat.index2word(idx) for idx in idx_concave]
    dist  = geodesic_dist[CONCAVE_MASK]
    time  = [T[idx] for idx in MIN_IDX[CONCAVE_MASK]]

    print vocab[:20], dist[:20], time[:20]
    exit()

    return SL, vocab, dist, time

    '''
    while True:
        print geodesic_dist
        exit()

        best_idx  = np.argsort(geodesic_dist)[:slurp_n]
        
        result = [[feat.index2word(idx), geodesic_dist[idx]]
                  for idx in best_idx]

        for idx in best_idx:
            word = feat.index2word(idx)
            WL[word][t] = geodesic_dist[idx]

    return SL,WL
    '''

def refine_top_words(SL,WL):

    print WL
    print SL
    exit()

    TOP_WL = dict()

    for word in WL:
        max_val = min(WL[word].values())
        max_t = [key for key in WL[word]
                 if WL[word][key]==max_val][0]
        TOP_WL[word] = (max_t,max_val)

    df = pd.DataFrame(index=TOP_WL.keys(),
                      columns=("t","dist"))
    for key in TOP_WL:
        df.ix[key] = TOP_WL[key]

    df.sort(["t","dist"],ascending=[1,0],inplace=True)
    return df


#w1,w2 = "run","walk"
#w1,w2="teacher","scientist"
w1,w2="fate","destiny"

lf = build_local_features(w1,w2,features, n_local=3000)
SL,WL = slerp_word_path(w1,w2,lf)
exit()
#df = refine_top_words(SL,WL)

for word in df.index:

    time = df["t"][word]
    distance = df["dist"][word]

    if distance < 1.1:
        print "{:0.5f} {:0.3f} {}".format(time, distance, word)

