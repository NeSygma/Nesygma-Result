fof(premise1, axiom, ! [P] : (spills_lots_of_food(P) => ~notably_tidy(P))).
fof(premise3, axiom, ! [P] : (cleanly(P) => notably_tidy(P))).
fof(premise6, axiom, (spills_lots_of_food(peter) & cleanly(peter)) | (~spills_lots_of_food(peter) & ~cleanly(peter))).
fof(goal, conjecture, notably_tidy(peter)).