% Positive version: original conclusion as conjecture
% Premise 1: All cats are mammals.
fof(premise1, axiom, ! [X] : (cat(X) => mammal(X))).
% Premise 2: Some pets are not mammals.
fof(premise2, axiom, ? [X] : (pet(X) & ~mammal(X))).
% Conclusion: No pets are cats. i.e., For all X, if X is a pet then X is not a cat.
fof(conclusion, conjecture, ! [X] : (pet(X) => ~cat(X))).