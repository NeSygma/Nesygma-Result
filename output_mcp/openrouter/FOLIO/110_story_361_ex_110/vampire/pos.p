% Positive version
fof(rule1, axiom, ![X] : (spill_lot(X) => ~notably_tidy(X))).
fof(rule2, axiom, ![X] : (clumsy_foodie_go_out(X) => spill_lot(X))).
fof(rule3, axiom, ![X] : (cleanly(X) => notably_tidy(X))).
fof(rule4, axiom, ![X] : (value_order_spotless(X) => cleanly(X))).
fof(rule5, axiom, ![X] : (family_prioritizes_order_spotless(X) => value_order_spotless(X))).
fof(peter_case, axiom, (spill_lot(peter) & cleanly(peter)) | (~spill_lot(peter) & ~cleanly(peter))).
fof(goal, conjecture, (clumsy_foodie_go_out(peter) & family_prioritizes_order_spotless(peter)) | (~clumsy_foodie_go_out(peter) & ~family_prioritizes_order_spotless(peter))).