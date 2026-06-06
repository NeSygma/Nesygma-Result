% Positive test: some affection is positive
fof(premise1, axiom, ? [X] : (affection(X) & love(X))).
fof(premise2, axiom, ? [X] : (love(X) & positive(X))).
fof(goal, conjecture, ? [X] : (affection(X) & positive(X))).