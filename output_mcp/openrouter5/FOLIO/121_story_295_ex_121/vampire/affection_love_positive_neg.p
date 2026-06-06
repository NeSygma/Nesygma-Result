% Negative version: negated claim as conjecture
% Premises:
% Some affection is love.
% Some love is positive.
% Negated conclusion: No affection is positive.

fof(premise1, axiom, ? [X] : (affection(X) & love(X))).
fof(premise2, axiom, ? [Y] : (love(Y) & positive(Y))).

fof(goal, conjecture, ~ ? [Z] : (affection(Z) & positive(Z))).