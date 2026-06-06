fof(premise_1, axiom, is_netflix_show(stranger_things)).
fof(premise_2, axiom, is_popular(stranger_things)).
fof(premise_3, axiom, ! [S] : ((is_netflix_show(S) & is_popular(S)) => binge_watches(karen, S))).
fof(premise_4, axiom, ! [S] : (binge_watches(karen, S) <=> downloads(karen, S))).
fof(premise_5, axiom, ~downloads(karen, black_mirror)).
fof(premise_6, axiom, is_netflix_show(black_mirror)).
fof(premise_7, axiom, ! [S] : (binge_watches(karen, S) => shares_with(karen, S, lisa))).
fof(conclusion_negation, conjecture, ~shares_with(karen, black_mirror, lisa)).