% Negative version: Peter is NOT either both or neither (i.e., exactly one is true)
fof(premise_1, axiom, ! [X] : (spills_lot(X) => ~tidy(X))).
fof(premise_2, axiom, ! [X] : (clumsy_foodie(X) => spills_lot(X))).
fof(premise_3, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(premise_4, axiom, ! [X] : (values_order(X) => cleanly(X))).
fof(premise_5, axiom, ! [X] : (family_prioritizes_order(X) => values_order(X))).
fof(premise_6, axiom, (spills_lot(peter) & cleanly(peter)) | (~spills_lot(peter) & ~cleanly(peter))).
fof(distinct_names, axiom, peter != a & peter != b). % Ensure peter is distinct
fof(goal_negation, conjecture, ~((clumsy_foodie(peter) & family_prioritizes_order(peter)) | (~clumsy_foodie(peter) & ~family_prioritizes_order(peter)))).