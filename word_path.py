import sqlite3
import itertools
import numpy as np

from gensim.models.word2vec import Word2Vec

print "Loading features..."
f_features = "db/features.word2vec"
features = Word2Vec.load(f_features)
features.init_sims()


def closest_approach(w1,w2):
    ''' 
    Define a line segement, L between the two input vectors x1,x2.
    Parameterize the line by t, that linearly goes from 0->1 as x1->x2.
    For each point in the matrix A, return the distance to the line d,
    and where along the line t.
    '''

    X0 = features.syn0norm
    x1 = features[w1]
    x2 = features[w2]

    x21 = x2-x1
    x21_norm = np.linalg.norm(x21)

    X10 = x1-X0
    X10_21 = X10.dot(x21)

    T   = -X10_21 / x21_norm**2

    X10_norm = np.linalg.norm(X10,axis=1)

    D2  = (X10_norm*x21_norm)**2 - X10_21**2
    D2 /=  x21_norm**2

    # Fix near zeros
    epsilon = 10**(0.0)
    D = np.sqrt(D2+epsilon)

    return D, T



word_pairs = [
    ["boy","man"],
    ["teacher", "scientist"],
    ["black","white",],
    ["soft","hard"],
    ["girl","woman"],
    ["fate","destiny"],
    ["mind","body"],
    ["Obama","Bush",],
    ["conservative","liberal"],
    ["religion","rationalism"],
]

for w1, w2 in word_pairs:
    D,T = closest_approach(w1,w2)


    word_cutoff = 25
    close_idx = np.argsort(D)[:word_cutoff]
    WORDS = np.array([features.index2word[idx] for idx in close_idx])
    timeline = T[close_idx]
    dist = D[close_idx]

    chrono_idx = np.argsort(timeline)
    timeline = timeline[chrono_idx]
    WORDS = WORDS[chrono_idx]
    dist = dist[chrono_idx]

    print

    for w,t,d in zip(WORDS, timeline, dist):
        print "{:0.5f}, {} ({:0.3f})".format(t, w, d)


