% Positive version: original claim as conjecture
% Premises:
% 1. A hawk never swims.
% 2. Some birds are hawks.
% Conclusion: All birds swim.

fof(hawk_no_swim, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(some_birds_are_hawks, axiom, ? [X] : (bird(X) & hawk(X))).

fof(goal, conjecture, ! [X] : (bird(X) => swims(X))).