fof(exists_growth_stock, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(growth_to_bought, axiom, ! [X] : (growth_stock(X) => bought_to_earn_profits_from_rapid_price_appreciation(X))).
fof(bought_to_not_suitable, axiom, ! [X] : (bought_to_earn_profits_from_rapid_price_appreciation(X) => ~suitable_for_retirement_fund(X))).
fof(mature_to_suitable, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).
fof(ko_mature, axiom, mature_stock(ko)).
fof(goal, conjecture, ~ (stock(ko) & growth_stock(ko))).