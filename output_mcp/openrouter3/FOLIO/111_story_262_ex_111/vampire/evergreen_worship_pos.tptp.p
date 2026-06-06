% Premises
fof(premise_1, axiom, ! [X] : (fir_tree(X) => evergreen(X))).
fof(premise_2, axiom, ? [X] : (object_of_worship(X) & fir_tree(X))).

% Conclusion to evaluate
fof(conclusion, conjecture, ? [X] : (evergreen(X) & ~object_of_worship(X))).