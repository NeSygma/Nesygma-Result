fof(all_growth_bought, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_appreciation(X))).
fof(bought_not_suitable, axiom, ! [X] : (bought_for_rapid_appreciation(X) => ~suitable_for_retirement(X))).
fof(some_growth, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(mature_suitable, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).
fof(ko_mature, axiom, mature_stock(ko)).
fof(mature_implies_stock, axiom, ! [X] : (mature_stock(X) => stock(X))).
fof(goal, conjecture, (stock(ko) & growth_stock(ko))).