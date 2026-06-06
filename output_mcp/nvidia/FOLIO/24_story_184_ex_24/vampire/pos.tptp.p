fof(axiom_1, axiom, popular(stranger_things)).
fof(axiom_2, axiom, netflix_show(stranger_things)).
fof(axiom_3, axiom, ! [X] : (netflix_show(X) & popular(X) => binge_watches(karen, X))).
fof(axiom_4, axiom, ! [X] : (netflix_show(X) & binge_watches(karen, X) => downloads(karen, X))).
fof(axiom_5, axiom, ! [X] : (netflix_show(X) & downloads(karen, X) => binge_watches(karen, X))).
fof(axiom_6, axiom, ~ downloads(karen, black_mirror)).
fof(axiom_7, axiom, netflix_show(black_mirror)).
fof(axiom_8, axiom, ! [X] : (netflix_show(X) & binge_watches(karen, X) => shares(karen, X, lisa))).
fof(distinct_axiom, axiom, (stranger_things != black_mirror & stranger_things != karen & stranger_things != lisa & black_mirror != karen & black_mirror != lisa & karen != lisa)).
fof(conjecture, conjecture, shares(karen, black_mirror, lisa)).