% Negative run: negated claim as conjecture
% Premise 1
fof(premise_1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
% Premise 2
fof(premise_2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
% Premise 3
fof(premise_3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
% Premise 4
fof(premise_4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
% Premise 5: No chemical compounds contain only one element
fof(premise_5, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
% Premise 6: The mixture either both is a chemical compound and contains only one element, or neither
fof(premise_6, axiom, (chemical_compound(mixture) <=> contains_only_one_element(mixture))).

% Negated conclusion: It is NOT the case that (the mixture is an alkane and contains carbon)
fof(neg_conclusion, conjecture, ~(alkane(mixture) & contains_carbon(mixture))).