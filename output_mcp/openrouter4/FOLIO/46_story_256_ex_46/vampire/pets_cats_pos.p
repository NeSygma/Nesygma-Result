% Positive test: original claim as conjecture
% Premise 1: All cats are mammals.
fof(premise1, axiom, ! [X] : (cat(X) => mammal(X))).
% Premise 2: Some pets are not mammals.
fof(premise2, axiom, ? [X] : (pet(X) & ~mammal(X))).
% Conclusion: No pets are cats.  (i.e., all pets are non-cats)
fof(conclusion, conjecture, ! [X] : (pet(X) => ~cat(X))).