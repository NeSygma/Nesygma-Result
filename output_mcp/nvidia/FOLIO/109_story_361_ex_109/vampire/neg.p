fof(premise1, axiom, ! [X] : (spill_lot(X) => ~tidy(X))).
fof(premise2, axiom, ! [X] : (clumsy_foodie(X) => spill_lot(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(premise4, axiom, ! [X] : (values_order_spotlessness(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes(X) => values_order_spotlessness(X))).
fof(peter_cases, axiom, (spill_lot(peter) & cleanly(peter)) | (~spill_lot(peter) & ~cleanly(peter))).
fof(neg_conjecture, conjecture, ~(clumsy_foodie(peter) | family_prioritizes(peter))).