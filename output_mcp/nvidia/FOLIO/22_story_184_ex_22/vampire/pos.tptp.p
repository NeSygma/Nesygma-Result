fof(prem1, axiom, netflix_show(stranger_things) & popular(stranger_things)).
fof(prem2, axiom, ! [X] : ((netflix_show(X) & popular(X)) => binge(karen, X))).
fof(prem3a, axiom, ! [X] : ((netflix_show(X) & binge(karen, X)) => download(karen, X))).
fof(prem3b, axiom, ! [X] : ((download(karen, X) => netflix_show(X) & binge(karen, X))) ).
fof(prem4, axiom, ~download(karen, black_mirror)).
fof(prem5, axiom, netflix_show(black_mirror)).
fof(prem6, axiom, ! [X] : ((netflix_show(X) & binge(karen, X)) => share(karen, X, lisa))).
fof(conclusion, conjecture, share(karen, stranger_things, lisa)).