## transorthogonal-linguistics
_[Travis Hoppe](http://thoppe.github.io/)_

If heroku is running, checkout the live demo (it may take 30 seconds to warm up):

   
[https://transorthogonal-linguistics.herokuapp.com/](https://transorthogonal-linguistics.herokuapp.com/)

### Introduction
  
Words rarely exist in a vacuum.
To understand the meaning of the word cat,
  it's useful to know that it _is_ ([hypernym](https://en.wikipedia.org/wiki/Hyponymy_and_hypernymy)) an animal,
  that it  _is the same as_ ([synonym](https://en.wikipedia.org/?title=Synonym)) a feline,
  that a Tabby is _a type of_ ([hyponym](https://en.wikipedia.org/wiki/Hyponymy_and_hypernymy)) cat,
  and that in some reasonable sense it is the _opposite_ ([antonym](https://en.wikipedia.org/wiki/Opposite_(semantics))) of a dog.
  Since words are connected in a rich network of linguisitic information, why not (literally) follow that path and see where it takes us?

Instead of looking at a single word in isolation, this project tries elucidate what words should be _in between_ a start and end word.

Grouping words together is a classic problem in computational linguisitics.
Typical approaches use [LSA](https://en.wikipedia.org/wiki/Latent_semantic_analysis), [LSI](https://en.wikipedia.org/wiki/Latent_semantic_indexing), [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) or [Pachinko allocation](https://en.wikipedia.org/wiki/Pachinko_allocation).
Personally, I perfer [Word2Vec](https://code.google.com/p/word2vec/) which was developed by some lovely engineers from Google. Partly because there exists an excellent port to Python via [gensim](https://radimrehurek.com/gensim/models/word2vec.html), but mostly because it's awesome.

  Word2Vec maps each word to a point on a unit [hypersphere](http://mathworld.wolfram.com/Hypersphere.html).
  Words that are "[close](https://en.wikipedia.org/wiki/Cosine_similarity)" on this sphere often share some kind of semantic relation.
  If we pick two words, say "boy" and "man", we can trace the shortest [path](https://en.wikipedia.org/?title=Geodesic) that connects them.
  We parameterize this curve with a "time" where t=0 (at boy) and t=1 (at man).
  Words that are close to this timeline are selected and ordered by their t value (e.g. to the t where they are closest to the connecting curve).
  In theory, this timeline should be a semantic map from one word to another -- smoothly varying across meaning.

  In practice however, it turns out that computing the true curve across the hypersphere is rather tricky. It's even harder to numerically find the nearest points efficiently.
  However if we cheat a little, we can draw a straight line connecting the two points as an approximation to the curve.
  If we do this, the problem reduces down to a fast linear algebra solution.
  Since we are moving across (trans) the orthogonal space spanned by the word2vec's construction, we call this method **transorthogonal linguistics**.

### Data construction
  
  The database contained within this repo was constructed from a full English dump of Wikipedia that was sentence and word tokenized by [NLTK](http://www.nltk.org/).
  Word2Vec training was done with a single pass, 300 dimensions and an 800 minimum vocabulary count.
  These choices were found to be optimal for the results, yet still be small enough to query online reasonably quickly.

### Command-line interface

    python transorthogonal_linguistics/word_path.py boy man

### Examples

With the input of `boy` and `man` we get:

#### `boy` to `man`

    boy
    - 
    sixteen-year-old, orphan
    teenager, girl, schoolgirl
    youngster, shepherd, lad, kid
    kitten, lonely, maid
    beggar, policeman
    prostitute, thug, villager, handsome, loner, thief, cop
    gentleman, stranger, lady, Englishman, guy
    -
    woman
    person
    man

#### `sun` to `moon` 
  
    sun
    sunlight, mist
    glow, shine, clouds
    skies, shines, shining, glare, moonlight, sky, darkness
    shadows, heavens
    horizon, crescent
    earth, eclipses
    constellations, comet, planets, orbits, orbiting, Earth, Io
    Jupiter, planet, Venus, Pluto, Uranus, orbit
    -
    moons, lunar
    moon
  

Other interesting examples:
  
    girl woman
    lover sinner
    fate destiny
    god demon
    good bad
    mind body
    heaven hell
    American Soviet
    idea action    
    socialism capitalism
    Marxism Stalinism
    man machine
    sustenance starvation
    war peace
    predictable idiosyncratic
    acceptance uproar
