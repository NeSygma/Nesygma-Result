% Negative file: negated conclusion as conjecture
fof(premise1, axiom, ! [X] : (fir_tree(X) => evergreen(X))).
fof(premise2, axiom, ? [X] : (object_of_worship(X) & fir_tree(X))).
fof(negated_conclusion, conjecture, ! [X] : (evergreen(X) => object_of_worship(X))).