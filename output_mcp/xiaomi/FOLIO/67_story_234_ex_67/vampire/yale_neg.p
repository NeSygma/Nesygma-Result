fof(yale_endowment_val, axiom, endowment_value(yale)).
fof(largest_def, axiom, ! [X] : (largest_endowment(X) <=> 
    (endowment_value(X) & ! [Y] : ((endowment_value(Y) & Y != X) => endowment_greater(X, Y))))).
fof(goal, conjecture, ~largest_endowment(yale)).