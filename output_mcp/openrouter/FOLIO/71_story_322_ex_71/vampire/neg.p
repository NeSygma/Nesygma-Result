fof(premise1, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_appreciation(X))).
fof(premise2, axiom, ! [X] : (bought_for_rapid_appreciation(X) => ~suitable_for_retirement_fund(X))).
fof(premise3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(premise4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).
fof(premise5, axiom, mature_stock(ko)).
fof(conj, conjecture, ~stock(ko)).