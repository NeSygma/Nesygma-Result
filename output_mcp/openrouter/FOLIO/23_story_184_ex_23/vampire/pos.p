% Positive version
fof(distinct_consts, axiom, (stranger_things != black_mirror & stranger_things != karen & stranger_things != lisa & black_mirror != karen & black_mirror != lisa & karen != lisa)).

fof(premise1, axiom, (popular(stranger_things) & netflix_show(stranger_things))).
fof(premise2, axiom, ! [X] : ((netflix_show(X) & popular(X)) => binge(karen, X))).
fof(premise3, axiom, ! [X] : (netflix_show(X) => (binge(karen, X) <=> download(karen, X)))).
fof(premise4, axiom, ~download(karen, black_mirror)).
fof(premise5, axiom, netflix_show(black_mirror)).
fof(premise6, axiom, ! [X] : ((netflix_show(X) & binge(karen, X)) => share(karen, X, lisa))).

fof(goal, conjecture, popular(black_mirror)).