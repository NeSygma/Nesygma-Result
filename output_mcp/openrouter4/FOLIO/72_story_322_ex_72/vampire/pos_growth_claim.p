% Premise 1: All growth stocks are bought to earn profits from rapid price appreciation.
fof(premise_1, axiom, ! [X] : (growth_stock(X) => bought_for_profits(X))).

% Premise 2: If bought for rapid price appreciation, then not suitable for retirement.
fof(premise_2, axiom, ! [X] : (bought_for_profits(X) => ~suitable_for_retirement(X))).

% Premise 3: Some stocks are growth stocks.
fof(premise_3, axiom, ? [X] : (stock(X) & growth_stock(X))).

% Premise 4: All mature stocks are suitable for a retirement fund.
fof(premise_4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).

% Premise 5: KO is a mature stock.
fof(premise_5, axiom, mature_stock(ko)).

% Natural subsumption: a mature stock is a stock.
fof(subsumption, axiom, ! [X] : (mature_stock(X) => stock(X))).

% Distinguish KO from any other constants (none others, so no inequality needed).

% Conclusion to evaluate: KO is a stock and a growth stock.
fof(goal, conjecture, (stock(ko) & growth_stock(ko))).