% Negative test: Is the negation of the conclusion entailed?
% Premise 1: Some mammals have teeth.
fof(some_mammals_have_teeth, axiom, ? [X] : (mammal(X) & has_teeth(X))).
% Premise 2: Platypuses have no teeth.
fof(platypus_no_teeth, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
% Premise 3: Platypuses are mammals.
fof(platypus_are_mammals, axiom, ! [X] : (platypus(X) => mammal(X))).
% Premise 4: Humans have teeth.
fof(humans_have_teeth, axiom, ! [X] : (human(X) => has_teeth(X))).

% Negated conclusion: There exists a platypus that is not a mammal or has teeth.
fof(negated_conclusion, conjecture, ? [X] : (platypus(X) & (~mammal(X) | has_teeth(X)))).