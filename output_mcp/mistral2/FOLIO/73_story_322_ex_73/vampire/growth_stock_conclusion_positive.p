fof(all_growth_are_bought_for_profit, axiom,
    ! [X] : (growth_stock(X) => bought_for_rapid_profit(X))).

fof(bought_for_profit_implies_not_suitable, axiom,
    ! [X] : (bought_for_rapid_profit(X) => ~suitable_for_retirement_fund(X))).

fof(some_stocks_are_growth, axiom,
    ? [X] : (stock(X) & growth_stock(X))).

fof(all_mature_are_suitable, axiom,
    ! [X] : (mature_stock(X) => suitable_for_retirement_fund(X))).

fof(ko_is_mature, axiom,
    mature_stock(ko)).

fof(ko_is_stock, axiom,
    stock(ko)).

fof(conclusion, conjecture,
    (growth_stock(ko) | bought_for_rapid_profit(ko)) =>
    (~stock(ko) & ~volatile_price(ko))).