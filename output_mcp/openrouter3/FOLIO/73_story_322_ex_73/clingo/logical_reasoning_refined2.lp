% Logical Reasoning Problem: Growth Stocks and Retirement Funds

% Domain declarations
stock(ko).
stock(X) :- growth_stock(X).
stock(X) :- mature_stock(X).

% Premise 1: All growth stocks are bought to earn profits from rapid price appreciation.
% This means: if growth_stock(X) then bought_for_appreciation(X)
growth_stock(X) :- bought_for_appreciation(X).

% Premise 2: If bought for appreciation, then not suitable for retirement fund.
:- bought_for_appreciation(X), suitable_for_retirement(X).

% Premise 3: Some stocks are growth stocks.
{growth_stock(X)} :- stock(X).

% Premise 4: All mature stocks are suitable for retirement fund.
suitable_for_retirement(X) :- mature_stock(X).

% Premise 5: KO is a mature stock.
mature_stock(ko).

% Additional domain: price volatility (open relation)
{price_volatile(X)} :- stock(X).

% Define bought_for_appreciation as an open relation (since it's not fully determined by premises)
{bought_for_appreciation(X)} :- stock(X).

% Deductions from premises:
% From premise 5: KO is mature, so suitable_for_retirement(ko) (from premise 4)
suitable_for_retirement(ko).

% From premise 2: If bought_for_appreciation(ko) then not suitable_for_retirement(ko)
% But we have suitable_for_retirement(ko), so by contrapositive, not bought_for_appreciation(ko)
% We can encode this as a constraint:
:- bought_for_appreciation(ko).

% From premise 1: If growth_stock(ko) then bought_for_appreciation(ko)
% Since not bought_for_appreciation(ko), then not growth_stock(ko)
% We can encode this as a constraint:
:- growth_stock(ko).

% Now, the antecedent of the conclusion: growth_stock(ko) OR bought_for_appreciation(ko)
% Since both are false, the antecedent is false.

% Conclusion evaluation
% The conclusion is: If (KO is growth stock OR bought for appreciation) THEN (KO is not a stock AND not price volatile)
% Let's break this down:
% 1. Antecedent: growth_stock(ko) OR bought_for_appreciation(ko)
% 2. Consequent: NOT stock(ko) AND NOT price_volatile(ko)

% Define the antecedent (using separate rules for OR)
conclusion_antecedent :- growth_stock(ko).
conclusion_antecedent :- bought_for_appreciation(ko).

% Define the consequent
conclusion_consequent :- not stock(ko), not price_volatile(ko).

% Independent derivation for conclusion being true
% The conclusion is true if either antecedent is false OR consequent is true
% But we need to derive it positively from premises.
% Since antecedent is false (from deductions), the implication is true.
% We can derive conclusion_true as: not conclusion_antecedent OR conclusion_consequent
% But we need positive derivation. Let's derive conclusion_true when antecedent is false.
conclusion_true :- not conclusion_antecedent.

% Independent derivation for conclusion being false
% The conclusion is false only if antecedent is true AND consequent is false
conclusion_false :- conclusion_antecedent, not conclusion_consequent.

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

% Show the answer
#show answer/1.