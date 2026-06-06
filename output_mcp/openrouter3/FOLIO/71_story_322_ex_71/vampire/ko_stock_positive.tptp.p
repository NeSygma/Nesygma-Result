fof(premise_1, axiom, ! [X] : (growth_stock(X) => bought_for_appreciation(X))).
fof(premise_2, axiom, ! [X] : (bought_for_appreciation(X) => ~suitable_for_retirement(X))).
fof(premise_3, axiom, ? [X] : (growth_stock(X) & stock(X))).
fof(premise_4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).
fof(premise_5, axiom, mature_stock(ko)).
fof(goal, conjecture, stock(ko)).