fof(premise_all_fir_are_evergreen, axiom, ! [X] : (fir_tree(X) => evergreen(X))).
fof(premise_some_worship_are_fir, axiom, ? [X] : (object_of_worship(X) & fir_tree(X))).
fof(conclusion_some_evergreen_not_worship, conjecture, ~(? [X] : (evergreen(X) & ~object_of_worship(X)))).