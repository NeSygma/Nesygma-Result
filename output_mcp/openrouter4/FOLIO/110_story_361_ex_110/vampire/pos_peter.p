fof(axiom1, axiom, ! [X] : (spill_food(X) => ~tidy(X))).
fof(axiom2, axiom, ! [X] : (clumsy_foodie(X) => spill_food(X))).
fof(axiom3, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(axiom4, axiom, ! [X] : (values_order(X) => cleanly(X))).
fof(axiom5, axiom, ! [X] : (family_prioritizes(X) => values_order(X))).
fof(axiom6, axiom, (spill_food(peter) & cleanly(peter)) | (~spill_food(peter) & ~cleanly(peter))).
fof(conclusion, conjecture, (clumsy_foodie(peter) & family_prioritizes(peter)) | (~clumsy_foodie(peter) & ~family_prioritizes(peter))).