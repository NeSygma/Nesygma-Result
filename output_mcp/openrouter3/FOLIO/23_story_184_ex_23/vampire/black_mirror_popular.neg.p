% Problem: Black Mirror popularity evaluation
% Negative version: Black Mirror is NOT popular

fof(distinct_entities, axiom, 
    (netflix_show_stranger_things != netflix_show_black_mirror & 
     netflix_show_stranger_things != karen &
     netflix_show_stranger_things != lisa &
     netflix_show_black_mirror != karen &
     netflix_show_black_mirror != lisa &
     karen != lisa)).

fof(premise_1, axiom, popular(netflix_show_stranger_things)).

fof(premise_2, axiom, 
    ! [X] : (netflix_show(X) & popular(X) => binge_watches(karen, X))).

fof(premise_3, axiom, 
    ! [X] : (binge_watches(karen, X) <=> downloads(karen, X))).

fof(premise_4, axiom, ~downloads(karen, netflix_show_black_mirror)).

fof(premise_5, axiom, netflix_show(netflix_show_black_mirror)).

fof(premise_6, axiom, 
    ! [X] : (binge_watches(karen, X) => shares(karen, X, lisa))).

fof(goal, conjecture, ~popular(netflix_show_black_mirror)).