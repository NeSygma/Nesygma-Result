% Negative file: negated claim as conjecture
fof(premise1, axiom, ! [X] : (spills_lot(X) => ~notably_tidy(X))).
fof(premise2, axiom, ! [X] : ((clumsy_foodie(X) & goes_out_frequently(X)) => spills_lot(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise4, axiom, ! [X] : (values_order(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes(X) => values_order(X))).
fof(premise6, axiom, (spills_lot(peter) & cleanly(peter)) | (~spills_lot(peter) & ~cleanly(peter))).

fof(goal_neg, conjecture, ~notably_tidy(peter)).