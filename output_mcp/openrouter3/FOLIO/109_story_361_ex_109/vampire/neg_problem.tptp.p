% Premises
fof(rule_1, axiom, ! [X] : (spills_lot_food(X) => ~tidy(X))).
fof(rule_2, axiom, ! [X] : (clumsy_foodie(X) => spills_lot_food(X))).
fof(rule_3, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(rule_4, axiom, ! [X] : (values_order_spotlessness(X) => cleanly(X))).
fof(rule_5, axiom, ! [X] : (family_prioritizes_order_spotlessness(X) => values_order_spotlessness(X))).
fof(peter_fact, axiom, (spills_lot_food(peter) & cleanly(peter)) | (~spills_lot_food(peter) & ~cleanly(peter))).

% Negated conclusion
fof(goal_neg, conjecture, ~(clumsy_foodie(peter) | family_prioritizes_order_spotlessness(peter))).