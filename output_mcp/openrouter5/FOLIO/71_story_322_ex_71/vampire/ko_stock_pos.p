% Positive file: original claim as conjecture
% Premises:
% 1. All growth stocks are bought to earn profits from rapid price appreciation.
fof(premise1, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_appreciation(X))).

% 2. If the stock price is bought to earn profits from rapid price appreciation, then it is not suitable for a retirement fund.
fof(premise2, axiom, ! [X] : (bought_for_rapid_appreciation(X) => ~suitable_for_retirement(X))).

% 3. Some stocks are growth stocks.
fof(premise3, axiom, ? [X] : (stock(X) & growth_stock(X))).

% 4. All mature stocks are suitable for a retirement fund.
fof(premise4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).

% 5. KO is a mature stock.
fof(premise5, axiom, mature_stock(ko)).

% Conclusion: KO is a stock.
fof(conclusion, conjecture, stock(ko)).