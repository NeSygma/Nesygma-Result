fof(all_fir_are_evergreen, axiom, ! [X] : (fir_tree(X) => evergreen(X))).
fof(some_worship_are_fir, axiom, ? [X] : (object_of_worship(X) & fir_tree(X))).
fof(conclusion_negation, conjecture, ~(? [X] : (evergreen(X) & ~object_of_worship(X)))).