% Growth Stock Problem - Positive Version
% Premises
fof(premise_1, axiom, ! [X] : (growth_stock(X) => bought_for_appreciation(X))).
fof(premise_2, axiom, ! [X] : (bought_for_appreciation(X) => ~suitable_for_retirement(X))).
fof(premise_3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(premise_4, axiom, ! [X] : (mature_stock(X) => suitable_for_retirement(X))).
fof(premise_5, axiom, mature_stock(ko)).

% Distinctness (though only one constant here)
fof(distinct, axiom, ko = ko).

% Conclusion to evaluate
fof(conclusion, conjecture, stock(ko) & growth_stock(ko)).