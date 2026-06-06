fof(premise1, axiom, ! [X] : (spills_lots_of_food(X) => ~notably_tidy(X))).
fof(premise2, axiom, ! [X] : (clumsy_foodies(X) => spills_lots_of_food(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise4, axiom, ! [X] : (values_order_and_spotlessness(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes_order_and_spotlessness(X) => values_order_and_spotlessness(X))).
fof(peter_statement, axiom, (spills_lots_of_food(peter) & cleanly(peter)) | (~spills_lots_of_food(peter) & ~cleanly(peter))).
fof(conclusion, conjecture, clumsy_foodies(peter) | family_prioritizes_order_and_spotlessness(peter)).