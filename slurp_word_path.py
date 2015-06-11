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

def slerp_points(wa,wb,feat,slurp_n=10):
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

def slerp_word_path(w0,w1,feat,slurp_n=15,vec_n=20):

    vec_n += 1
    T  = np.linspace(0,1,vec_n)

    SL = slerp_points(w0,w1,feat,slurp_n)
    WL = collections.defaultdict(dict)

    for k,L in enumerate(SL):
        t = float(k)/(SL.shape[0]-1)
        #print "Computing SLURP {}".format(k)

        cosine_dist   = np.dot(feat.features, L)
        cosine_dist[cosine_dist>=1] = 1.0
        geodesic_dist = np.arccos(cosine_dist)

        best_idx  = np.argsort(geodesic_dist)[:slurp_n]
        
        result = [[feat.index2word(idx), geodesic_dist[idx]]
                  for idx in best_idx]

        for idx in best_idx:
            word = feat.index2word(idx)
            WL[word][t] = geodesic_dist[idx]

    return WL

def refine_top_words(WL):#,full_features):

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
WL = slerp_word_path(w1,w2,lf,vec_n=20,slurp_n=50)
df = refine_top_words(WL)

for word in df.index:

    time = df["t"][word]
    distance = df["dist"][word]

    if distance < 1.1:
        print "{:0.5f} {:0.3f} {}".format(time, distance, word)

