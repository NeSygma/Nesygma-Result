% Negative version: negated claim as conjecture
fof(premise_1, axiom, ! [X] : (istanbul_plate(X) => begins_with_34(X))).
fof(premise_2, axiom, ! [X] : (~begins_with_34(X) => ~istanbul_plate(X))).
fof(premise_3, axiom, istanbul_plate(joe)).
fof(premise_4, axiom, begins_with_35(tom)).
fof(premise_5, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).

fof(goal_neg, conjecture, ~begins_with_34(joe)).