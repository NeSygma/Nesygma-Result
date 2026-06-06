fof(prem1, axiom, ! [X] : (spills_food(X) => ~notably_tidy(X))).
fof(prem2, axiom, ! [X] : (clumsy_foodie(X) => spills_food(X))).
fof(prem3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(prem4, axiom, ! [X] : (values_order(X) => cleanly(X))).
fof(prem5, axiom, ! [X] : (family_prioritizes_order(X) => values_order(X))).
fof(prem6, axiom, ((spills_food(peter) & cleanly(peter)) | (~spills_food(peter) & ~cleanly(peter)))).
fof(goal, conjecture, clumsy_foodie(peter) | family_prioritizes_order(peter)).