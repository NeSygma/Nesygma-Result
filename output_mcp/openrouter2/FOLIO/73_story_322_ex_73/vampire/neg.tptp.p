fof(growth_to_bought, axiom, ! [S] : (growth_stock(S) => bought_to_earn_profits(S))).
fof(bought_not_retirement, axiom, ! [S] : (bought_to_earn_profits(S) => ~suitable_for_retirement_fund(S))).
fof(some_growth, axiom, ? [S] : (stock(S) & growth_stock(S))).
fof(mature_retirement, axiom, ! [S] : (mature_stock(S) => suitable_for_retirement_fund(S))).
fof(ko_mature, axiom, mature_stock(ko)).
fof(conjecture, conjecture, ((growth_stock(ko) | bought_to_earn_profits(ko)) & (stock(ko) | price_volatile(ko)))).