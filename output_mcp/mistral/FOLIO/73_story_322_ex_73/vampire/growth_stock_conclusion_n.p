fof(growth_implies_bought, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_profit_appreciation(X))).
fof(bought_implies_not_retirement, axiom, ! [X] : (bought_for_rapid_profit_appreciation(X) => ~suitable_for_retirement_fund(X))).
fof(some_growth_are_stocks, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(mature_implies_retirement, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).
fof(ko_is_mature, axiom, mature_stock(ko)).
fof(ko_is_stock, axiom, stock(ko)).
fof(negated_conclusion, conjecture, (growth_stock(ko) | bought_for_rapid_profit_appreciation(ko)) & (stock(ko) & volatile_price(ko))).