
def slerp_points(wa,wb,vector_n=10):
    ''' N-dimensional slerp interpolation '''
    va = features[wa]
    vb = features[wb]

    theta = np.arccos(va.dot(vb))
    st = np.sin(theta)

    T  = np.linspace(0,1,vector_n)
    L1 = np.sin((1-T)*theta)/st
    L2 = np.sin(T*theta)/st
    SL = np.outer(L1,va) + np.outer(L2,vb)
    
    return (SL.T / np.linalg.norm(SL,axis=1)).T

def slerp_word_path(w0,w1,vec_n=20,topn=15):

    vec_n += 1
    T  = np.linspace(0,1,vec_n)

    SL = slerp_points(w0,w1,vec_n)
    WL = collections.defaultdict(dict)

    for k,L in enumerate(SL):
        t = float(k)/(SL.shape[0]-1)
        print "Computing SLURP {}".format(k)

        cosine_dist = np.dot(features.syn0norm, L)
        geodesic_dist = np.arccos(cosine_dist)
        best_idx  = np.argsort(geodesic_dist)[:topn]
        
        result = [[features.index2word[idx], geodesic_dist[idx]]
                  for idx in best_idx]

        for idx in best_idx:
            word = features.index2word[idx]
            WL[word][t] = geodesic_dist[idx]

    TOP_WL = dict()

    for word in WL:
        max_val = min(WL[word].values())
        max_t = [key for key in WL[word] if WL[word][key]==max_val][0]
        TOP_WL[word] = (max_t,max_val)

    df = pd.DataFrame(index=TOP_WL.keys(),
                      columns=("t","dist"))
    for key in TOP_WL:
        df.ix[key] = TOP_WL[key]

    df.sort(["t","dist"],ascending=[1,0],inplace=True)
    return df


w0,w1="boy","man"
#w0,w1="teacher","scientist"
#w0,w1="teacher","scientist"
#w0,w1="day","night"
#print slerp_word_path(w0,w1,vec_n=15,topn=10)

#w0,w1="blue","green"
print slerp_word_path(w0,w1,vec_n=100,topn=25)
exit()
