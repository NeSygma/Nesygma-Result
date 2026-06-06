% Negative version: negated claim as conjecture
% Premises:
% 1. A hawk never swims.
% 2. Some birds are hawks.
% Negated conclusion: Not all birds swim (i.e., some bird does not swim)

fof(hawk_no_swim, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(some_birds_are_hawks, axiom, ? [X] : (bird(X) & hawk(X))).

fof(goal_neg, conjecture, ? [X] : (bird(X) & ~swims(X))).