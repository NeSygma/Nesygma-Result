% Peter's Tidiness Problem - Negative Version
% Premises
fof(premise_1, axiom, ! [X] : (spills_lot_food(X) => ~notably_tidy(X))).
fof(premise_2, axiom, ! [X] : (clumsy_foodie(X) => spills_lot_food(X))).
fof(premise_3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise_4, axiom, ! [X] : (values_order_spotlessness(X) => cleanly(X))).
fof(premise_5, axiom, ! [X] : (family_prioritizes_order(X) => values_order_spotlessness(X))).
fof(premise_6, axiom, (spills_lot_food(peter) & cleanly(peter)) | (~spills_lot_food(peter) & ~cleanly(peter))).

% Negated conclusion
fof(goal_negated, conjecture, ~notably_tidy(peter)).