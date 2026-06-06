fof(premise1, axiom, ! [X] : (growth_stock(X) => bought_for_appreciation(X))).
fof(premise2, axiom, ! [X] : (bought_for_appreciation(X) => ~suitable_for_retirement(X))).
fof(premise3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(premise4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).
fof(premise5, axiom, mature_stock(ko)).
fof(growth_stock_implies_stock, axiom, ! [X] : (growth_stock(X) => stock(X))).
fof(mature_stock_implies_stock, axiom, ! [X] : (mature_stock(X) => stock(X))).
fof(negated_conclusion, conjecture, (growth_stock(ko) | bought_for_appreciation(ko)) & (stock(ko) | price_volatile(ko))).