% Positive version: Conjecture is "Black Mirror is popular"
fof(premise_1, axiom, popular_show(stranger_things)).
fof(premise_2, axiom, ! [X] : ((netflix_show(X) & popular_show(X)) => binge_watch(karen, X))).
fof(premise_3, axiom, ! [X] : ((netflix_show(X) & binge_watch(karen, X)) <=> download(karen, X))).
fof(premise_4, axiom, ~download(karen, black_mirror)).
fof(premise_5, axiom, netflix_show(black_mirror)).
fof(premise_6, axiom, ! [X] : ((netflix_show(X) & binge_watch(karen, X)) => share_with(karen, X, lisa))).

fof(distinct, axiom, stranger_things != black_mirror).

fof(goal, conjecture, popular_show(black_mirror)).