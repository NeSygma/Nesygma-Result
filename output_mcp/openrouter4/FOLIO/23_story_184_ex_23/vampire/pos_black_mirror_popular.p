% Positive test: is "Black Mirror is popular" entailed?
fof(premise1a, axiom, netflix_show(stranger_things)).
fof(premise1b, axiom, popular(stranger_things)).

fof(premise2, axiom, ! [X] : 
    ((netflix_show(X) & popular(X)) => binge_watch(karen, X))).

fof(premise3, axiom, ! [X] : 
    (netflix_show(X) => (binge_watch(karen, X) <=> download(karen, X)))).

fof(premise4, axiom, ~download(karen, black_mirror)).

fof(premise5, axiom, netflix_show(black_mirror)).

fof(premise6, axiom, ! [X] : 
    ((netflix_show(X) & binge_watch(karen, X)) => share_with(karen, X, lisa))).

fof(distinct_shows, axiom, stranger_things != black_mirror).

fof(conclusion, conjecture, popular(black_mirror)).