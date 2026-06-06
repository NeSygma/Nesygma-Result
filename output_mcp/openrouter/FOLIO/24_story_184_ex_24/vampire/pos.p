fof(p1, axiom, netflix_show(stranger_things)).
fof(p2, axiom, popular(stranger_things)).
fof(p3, axiom, netflix_show(black_mirror)).
fof(p4, axiom, ~download(black_mirror)).
fof(p5, axiom, ![X] : ((netflix_show(X) & popular(X)) => binge(X))).
fof(p6, axiom, ![X] : (netflix_show(X) => (binge(X) <=> download(X)))).
fof(p7, axiom, ![X] : ((netflix_show(X) & binge(X)) => share(X))).
fof(distinct_shows, axiom, stranger_things != black_mirror).
fof(goal, conjecture, share(black_mirror)).