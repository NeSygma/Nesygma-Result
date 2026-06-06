fof(p1, axiom, ! [X] : (growth_stock(X) => bought_for_appreciation(X))).
fof(p2, axiom, ! [X] : (bought_for_appreciation(X) => ~suitable_for_retirement(X))).
fof(p3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(p4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).
fof(p5, axiom, mature_stock(ko)).
fof(tax1, axiom, ! [X] : (growth_stock(X) => stock(X))).
fof(tax2, axiom, ! [X] : (mature_stock(X) => stock(X))).
fof(goal, conjecture, stock(ko)).