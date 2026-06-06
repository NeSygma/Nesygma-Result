fof(all_growth_bought, axiom, ! [X] : (growth_stock(X) => bought_to_earn_profits_from_rapid_price_appreciation(X))).
fof(bought_not_retirement, axiom, ! [X] : (bought_to_earn_profits_from_rapid_price_appreciation(X) => ~suitable_for_retirement_fund(X))).
fof(some_growth_stock, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(all_mature_retirement, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).
fof(ko_mature, axiom, mature_stock(ko)).
fof(conjecture, conjecture, stock(ko)).