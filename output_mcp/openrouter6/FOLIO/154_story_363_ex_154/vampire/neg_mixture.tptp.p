% Negative file: negated conclusion as conjecture
fof(premise1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(premise2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(premise3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(premise4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(premise5, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
fof(premise6, axiom, chemical_compound(mix) <=> contains_only_one_element(mix)).
fof(neg_conclusion, conjecture, ~(alkane(mix) & contains_carbon(mix))).