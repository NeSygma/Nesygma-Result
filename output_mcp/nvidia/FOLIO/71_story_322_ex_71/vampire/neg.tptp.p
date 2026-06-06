fof(axiom_growth_to_earn, axiom, ! [X] : (growth_stock(X) => bought_to_earn(X))).
fof(axiom_earn_not_suitable, axiom, ! [X] : (bought_to_earn(X) => ~suitable_for_retirement_fund(X))).
fof(axiom_some_stocks_growth, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(axiom_mature_to_suitable, axiom, ! [X] : (mature(X) => suitable_for_retirement_fund(X))).
fof(axiom_ko_mature, axiom, mature(ko)).
fof(conclusion, conjecture, ~stock(ko)).