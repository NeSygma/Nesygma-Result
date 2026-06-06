% Negative version: negated conclusion as conjecture
% Premise 1: All cats are mammals.
fof(premise1, axiom, ! [X] : (cat(X) => mammal(X))).
% Premise 2: Some pets are not mammals.
fof(premise2, axiom, ? [X] : (pet(X) & ~mammal(X))).
% Negated conclusion: It is NOT the case that no pets are cats.
% i.e., There exists an X such that X is a pet and X is a cat.
fof(negated_conclusion, conjecture, ? [X] : (pet(X) & cat(X))).