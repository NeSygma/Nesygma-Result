fof(premise1, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_profit(X))).
fof(premise2, axiom, ! [X] : (bought_for_rapid_profit(X) => ~suitable_for_retirement_fund(X))).
fof(premise3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(premise4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).
fof(premise5, axiom, mature_stock(ko)).
fof(premise6, axiom, stock(ko)).
fof(conclusion, conjecture, growth_stock(ko)).