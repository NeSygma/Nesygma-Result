% Positive run
fof(distinct_consts, axiom, ko != s1).
fof(premise1, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_appreciation(X))).
fof(premise2, axiom, ! [X] : (bought_for_rapid_appreciation(X) => ~suitable_retirement_fund(X))).
fof(premise3, axiom, stock(s1) & growth_stock(s1)).
fof(premise4, axiom, ! [X] : (mature_stock(X) => suitable_retirement_fund(X))).
fof(premise5, axiom, mature_stock(ko)).
fof(conjecture, conjecture, (growth_stock(ko) | bought_for_rapid_appreciation(ko)) => (~stock(ko) & ~volatile_price(ko))).