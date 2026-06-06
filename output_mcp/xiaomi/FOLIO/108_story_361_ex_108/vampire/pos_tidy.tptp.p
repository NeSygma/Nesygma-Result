fof(premise1, axiom, ! [P] : (spills_a_lot(P) => ~notably_tidy(P))).
fof(premise2, axiom, ! [P] : ((clumsy_foodie(P) & goes_out_frequently(P)) => spills_a_lot(P))).
fof(premise3, axiom, ! [P] : (cleanly(P) => notably_tidy(P))).
fof(premise4, axiom, ! [P] : (values_order(P) => cleanly(P))).
fof(premise5, axiom, ! [P] : (family_priorizes_order(P) => values_order(P))).
fof(premise6, axiom, (spills_a_lot(peter) & cleanly(peter)) | (~spills_a_lot(peter) & ~cleanly(peter))).
fof(goal, conjecture, notably_tidy(peter)).