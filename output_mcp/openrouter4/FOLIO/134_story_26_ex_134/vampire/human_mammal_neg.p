% Premise 1: Some mammals have teeth.
fof(premise1, axiom, ? [X] : (mammal(X) & has_teeth(X))).
% Premise 2: Platypuses have no teeth.
fof(premise2, axiom, ! [X] : (platypus(X) => ~has_teeth(X))).
% Premise 3: Platypuses are mammals.
fof(premise3, axiom, ! [X] : (platypus(X) => mammal(X))).
% Premise 4: Humans have teeth.
fof(premise4, axiom, ! [X] : (human(X) => has_teeth(X))).
% Negated conclusion: There exists a human that is not a mammal.
fof(negated_conclusion, conjecture, ? [X] : (human(X) & ~mammal(X))).