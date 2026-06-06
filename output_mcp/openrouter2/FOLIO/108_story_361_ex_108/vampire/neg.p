fof(p1, axiom, ! [X] : (spills_food(X) => ~tidy(X))).
fof(p2, axiom, ! [X] : ((clumsy_foodie(X) & frequent_visitor(X)) => spills_food(X))).
fof(p3, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(p4, axiom, ! [X] : (value_order(X) => cleanly(X))).
fof(p5, axiom, ! [X] : (family_prioritizes_order(X) => value_order(X))).
fof(p6, axiom, ((spills_food(peter) & cleanly(peter)) | (~spills_food(peter) & ~cleanly(peter)))).
fof(goal, conjecture, ~tidy(peter)).