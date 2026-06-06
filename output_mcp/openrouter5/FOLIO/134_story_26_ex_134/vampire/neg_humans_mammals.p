% Negative file: negated claim as conjecture
% Premises:
% Some mammals have teeth.
% Platypuses have no teeth.
% Platypuses are mammals.
% Humans have teeth.
% Negated Conclusion: It is NOT the case that humans are mammals.

fof(some_mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(platypus_are_mammals, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(humans_have_teeth, axiom, ! [X] : (human(X) => has_teeth(X))).

fof(goal_neg, conjecture, ~! [X] : (human(X) => mammal(X))).