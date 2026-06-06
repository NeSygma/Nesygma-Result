fof(p1, axiom, ! [X] : (spill_food(X) => ~notably_tidy(X))).
fof(p2, axiom, ! [X] : (clumsy_foodie(X) => spill_food(X))).
fof(p3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(p4, axiom, ! [X] : (value_order(X) => cleanly(X))).
fof(p5, axiom, ! [X] : (family_prioritizes_order(X) => value_order(X))).
fof(p6, axiom, (spill_food(peter) & cleanly(peter)) | (~spill_food(peter) & ~cleanly(peter))).
fof(goal, conjecture, ~ (clumsy_foodie(peter) | family_prioritizes_order(peter))).