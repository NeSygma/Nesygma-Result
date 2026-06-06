% Negative version: negated conclusion as conjecture
% Predicates:
% growth_stock(X) - X is a growth stock
% bought_for_profits(X) - X is bought to earn profits from rapid price appreciation
% suitable_retirement(X) - X is suitable for a retirement fund
% mature_stock(X) - X is a mature stock
% stock(X) - X is a stock
% volatile_price(X) - X's price is volatile

% All growth stocks are bought to earn profits from rapid price appreciation.
fof(premise1, axiom, ! [X] : (growth_stock(X) => bought_for_profits(X))).

% If the stock price is bought to earn profits from rapid price appreciation, then it is not suitable for a retirement fund.
fof(premise2, axiom, ! [X] : (bought_for_profits(X) => ~suitable_retirement(X))).

% Some stocks are growth stocks.
fof(premise3, axiom, ? [X] : (stock(X) & growth_stock(X))).

% All mature stocks are suitable for a retirement fund.
fof(premise4, axiom, ! [X] : (mature_stock(X) => suitable_retirement(X))).

% KO is a mature stock.
fof(premise5, axiom, mature_stock(ko)).

% Distinctness (only one named entity)
fof(distinct, axiom, ko = ko).

% Negated conclusion: ~((growth_stock(ko) | bought_for_profits(ko)) => (~stock(ko) & ~volatile_price(ko)))
% Which is equivalent to: (growth_stock(ko) | bought_for_profits(ko)) & ~(~stock(ko) & ~volatile_price(ko))
% Which simplifies to: (growth_stock(ko) | bought_for_profits(ko)) & (stock(ko) | volatile_price(ko))
fof(neg_conclusion, conjecture, (growth_stock(ko) | bought_for_profits(ko)) & (stock(ko) | volatile_price(ko))).