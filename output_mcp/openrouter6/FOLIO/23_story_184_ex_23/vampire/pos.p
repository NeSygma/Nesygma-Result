fof(stranger_things_popular, axiom, popular(stranger_things) & netflix_show(stranger_things)).
fof(premise_2, axiom, ! [S] : (netflix_show(S) & popular(S) => binge_watches(karen, S))).
fof(premise_3, axiom, ! [S] : (binge_watches(karen, S) <=> downloads(karen, S))).
fof(premise_4, axiom, ~downloads(karen, black_mirror)).
fof(premise_5, axiom, netflix_show(black_mirror)).
fof(premise_6, axiom, ! [S] : (netflix_show(S) & binge_watches(karen, S) => shares(karen, S, lisa))).
fof(distinct_entities, axiom, (stranger_things != black_mirror & stranger_things != karen & stranger_things != lisa & black_mirror != karen & black_mirror != lisa & karen != lisa)).
fof(goal, conjecture, popular(black_mirror)).