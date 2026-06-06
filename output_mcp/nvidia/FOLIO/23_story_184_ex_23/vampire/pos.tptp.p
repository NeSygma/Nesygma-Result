fof(premise1, axiom, popular(stranger_things)).
fof(premise2, axiom, ! [X] : (netflix_show(X) & popular(X) => binge(X))).
fof(premise3, axiom, ! [X] : (binge(X) <=> download(X))).
fof(premise4, axiom, ~download(black_mirror)).
fof(premise5, axiom, netflix_show(black_mirror)).
fof(premise6, axiom, ! [X] : (netflix_show(X) & binge(X) => share(X))).
fof(goal, conjecture, popular(black_mirror)).