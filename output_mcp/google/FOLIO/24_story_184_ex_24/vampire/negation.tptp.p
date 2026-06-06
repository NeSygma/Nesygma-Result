fof(p1, axiom, is_netflix_show(stranger_things)).
fof(p2, axiom, ! [X] : ((is_netflix_show(X) & is_popular(X)) => binge_watches(karen, X))).
fof(p3, axiom, ! [X] : (is_netflix_show(X) => (binge_watches(karen, X) <=> downloads(karen, X)))).
fof(p4, axiom, ~downloads(karen, black_mirror)).
fof(p5, axiom, is_netflix_show(black_mirror)).
fof(p6, axiom, ! [X] : ((is_netflix_show(X) & binge_watches(karen, X)) => shares_with_lisa(karen, X))).
fof(goal, conjecture, ~shares_with_lisa(karen, black_mirror)).