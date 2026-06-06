% Negative test (negated conclusion)
fof(spill_not_tidy, axiom, ! [X] : (spill(X) => ~tidy(X))).
fof(clumsy_spill, axiom, ! [X] : (clumsy_foodie(X) => spill(X))).
fof(cleanly_tidy, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(value_cleanly, axiom, ! [X] : (value_order(X) => cleanly(X))).
fof(family_value, axiom, ! [X] : (family_prioritizes(X) => value_order(X))).
fof(peter_disj, axiom, (spill(peter) & cleanly(peter)) | (~spill(peter) & ~cleanly(peter))).
fof(goal_neg, conjecture, ~ (clumsy_foodie(peter) | family_prioritizes(peter))).