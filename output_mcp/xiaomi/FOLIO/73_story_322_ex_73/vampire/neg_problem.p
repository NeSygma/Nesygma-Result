% Premises
fof(p1, axiom, ! [X] : (growth_stock(X) => bought_for_profit(X))).
fof(p2, axiom, ! [X] : (bought_for_profit(X) => ~suitable_for_retirement(X))).
fof(p3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(p4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).
fof(p5, axiom, mature_stock(ko)).

% Negated conclusion
fof(goal, conjecture,
    ~((growth_stock(ko) | bought_for_profit(ko)) => (~stock(ko) & ~volatile(ko)))).