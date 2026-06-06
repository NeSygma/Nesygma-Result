% Negative version: negated conclusion as conjecture
% Conclusion: KO is a stock and a growth stock.
% Negated: ~(KO is a stock and a growth stock) i.e., ~stock(ko) | ~growth_stock(ko)

% All growth stocks are bought to earn profits from rapid price appreciation.
fof(premise_1, axiom, ! [X] : (growth_stock(X) => bought_for_rapid_appreciation(X))).

% If the stock price is bought to earn profits from rapid price appreciation, then it is not suitable for a retirement fund.
fof(premise_2, axiom, ! [X] : (bought_for_rapid_appreciation(X) => ~suitable_for_retirement(X))).

% Some stocks are growth stocks.
fof(premise_3, axiom, ? [X] : (stock(X) & growth_stock(X))).

% All mature stocks are suitable for a retirement fund.
fof(premise_4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).

% KO is a mature stock.
fof(premise_5, axiom, mature_stock(ko)).

% Mature stocks are stocks.
fof(premise_6, axiom, ! [X] : (mature_stock(X) => stock(X))).

% Negated conclusion: KO is NOT a stock OR KO is NOT a growth stock.
fof(negated_conclusion, conjecture, (~stock(ko) | ~growth_stock(ko))).