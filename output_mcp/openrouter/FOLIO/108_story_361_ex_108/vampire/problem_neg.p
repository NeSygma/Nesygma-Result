% Negative version (negated conclusion)
fof(premise1, axiom, ! [X] : (spill(X) => ~tidy(X))).
fof(premise2, axiom, ! [X] : (clumsy_foodie(X) => spill(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(premise4, axiom, ! [X] : (value_order(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritize_order(X) => value_order(X))).
fof(premise6, axiom, ( (spill(peter) & cleanly(peter)) | (~spill(peter) & ~cleanly(peter)) ) ).
fof(goal, conjecture, ~tidy(peter)).