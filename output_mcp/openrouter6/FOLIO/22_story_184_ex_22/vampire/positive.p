% Positive file: conclusion as conjecture
fof(distinct_constants, axiom, (karen != lisa & karen != stranger_things & karen != black_mirror & lisa != stranger_things & lisa != black_mirror & stranger_things != black_mirror)).
fof(premise_1, axiom, (netflix_show(stranger_things) & popular(stranger_things))).
fof(premise_2, axiom, ! [X] : (netflix_show(X) & popular(X) => binge_watch(karen, X))).
fof(premise_3, axiom, ! [X] : (netflix_show(X) => (binge_watch(karen, X) <=> download(karen, X)))).
fof(premise_4, axiom, ~download(karen, black_mirror)).
fof(premise_5, axiom, netflix_show(black_mirror)).
fof(premise_6, axiom, ! [X] : (netflix_show(X) & binge_watch(karen, X) => share(karen, lisa, X))).
fof(goal, conjecture, share(karen, lisa, stranger_things)).