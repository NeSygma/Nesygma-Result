fof(premise1, axiom, ! [X] : (spill_food(X) => ~notably_tidy(X))).
fof(premise2, axiom, ! [X] : (clumsy_foodie(X) => spill_food(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise4, axiom, ! [X] : (value_order_spotlessness(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes_order_spotlessness(X) => value_order_spotlessness(X))).
fof(premise6, axiom, (spill_food(peter) & cleanly(peter)) | (~spill_food(peter) & ~cleanly(peter))).
fof(goal, conjecture, ~notably_tidy(peter)).