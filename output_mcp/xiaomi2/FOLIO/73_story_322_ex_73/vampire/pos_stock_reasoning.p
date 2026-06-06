% Premises
fof(premise1, axiom, ! [X] : (growth_stock(X) => bought_for_profit(X))).
fof(premise2, axiom, ! [X] : (bought_for_profit(X) => ~suitable_for_retirement(X))).
fof(premise3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(premise4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).
fof(premise5, axiom, mature_stock(ko)).

% Conclusion: If KO is a growth stock or bought for profit, then KO is neither a stock nor price volatile
fof(goal, conjecture,
    ((growth_stock(ko) | bought_for_profit(ko)) => (~stock(ko) & ~price_volatile(ko)))).