fof(p1, axiom, ! [X] : (spill_food(X) => ~notably_tidy(X))).
fof(p2, axiom, ! [X] : ((clumsy_foodie(X) & goes_out_frequently(X)) => spill_food(X))).
fof(p3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(p4, axiom, ! [X] : (value_order_spotlessness(X) => cleanly(X))).
fof(p5, axiom, ! [X] : (family_prioritizes_order_spotlessness(X) => value_order_spotlessness(X))).
fof(p6, axiom, (spill_food(peter) & cleanly(peter)) | (~spill_food(peter) & ~cleanly(peter))).
fof(goal, conjecture, ~notably_tidy(peter)).