fof(premise1, axiom, ! [X] : (spill_lot(X) => ~notably_tidy(X))).
fof(premise2, axiom, ! [X] : (clumsy_foodie(X) => spill_lot(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise4, axiom, ! [X] : (value_order_spotless(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes_order_spotless(X) => value_order_spotless(X))).
fof(premise6, axiom, (spill_lot(peter) & cleanly(peter)) | (~spill_lot(peter) & ~cleanly(peter))).
fof(neg_conclusion, conjecture, ~(clumsy_foodie(peter) <=> family_prioritizes_order_spotless(peter))).