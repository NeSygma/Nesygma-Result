fof(axiom_growth_to_profits, axiom, ! [X] : (growth_stock(X) => bought_to_earn_profits_from_rapid_price_appreciation(X))).
fof(axiom_profits_not_retirement, axiom, ! [X] : (bought_to_earn_profits_from_rapid_price_appreciation(X) => ~suitable_for_retirement_fund(X))).
fof(axiom_some_stocks_growth, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(axiom_all_mature_retirement, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).
fof(axiom_ko_mature, axiom, mature_stock(ko)).
fof(negated_conclusion, conjecture, (growth_stock(ko) | bought_to_earn_profits_from_rapid_price_appreciation(ko)) & (stock(ko) | price_volatile(ko))).