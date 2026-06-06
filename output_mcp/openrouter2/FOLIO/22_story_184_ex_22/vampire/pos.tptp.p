fof(show1, axiom, netflix_show(stranger_things)).
fof(popular1, axiom, popular(stranger_things)).
fof(show2, axiom, netflix_show(black_mirror)).
fof(distinct, axiom, stranger_things != black_mirror).
fof(rule1, axiom, ![X] : ((netflix_show(X) & popular(X)) => binge_watch(karen, X))).
fof(rule2, axiom, ![X] : (binge_watch(karen, X) <=> download(karen, X))).
fof(rule3, axiom, ![X] : (binge_watch(karen, X) => share(karen, lisa, X))).
fof(no_download, axiom, ~download(karen, black_mirror)).
fof(goal, conjecture, share(karen, lisa, stranger_things)).