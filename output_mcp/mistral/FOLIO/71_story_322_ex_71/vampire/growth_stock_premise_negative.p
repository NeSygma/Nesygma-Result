fof(growth_stock_def, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_appreciation(X))).
fof(bought_rapid_app_not_retirement, axiom, ! [X] : (bought_for_rapid_appreciation(X) => ~suitable_for_retirement_fund(X))).
fof(some_growth_stocks, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(mature_retirement, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).
fof(ko_mature, axiom, mature_stock(ko)).
fof(goal_negation, conjecture, ~stock(ko)).