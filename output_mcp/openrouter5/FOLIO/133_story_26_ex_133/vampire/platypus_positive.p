% Positive file: original conclusion as conjecture
% Premises:
% Some mammals have teeth.
% Platypuses have no teeth.
% Platypuses are mammals.
% Humans have teeth.
% Conclusion: Platypuses are reptiles.

fof(some_mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
fof(platypus_no_teeth, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
fof(platypus_are_mammals, axiom, ! [X] : (platypus(X) => mammal(X))).
fof(humans_have_teeth, axiom, ! [X] : (human(X) => has_teeth(X))).

fof(conclusion, conjecture, ! [X] : (platypus(X) => reptile(X))).