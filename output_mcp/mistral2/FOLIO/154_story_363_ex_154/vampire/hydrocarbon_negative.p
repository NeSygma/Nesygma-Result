fof(premise1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(premise2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(premise3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(premise4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(premise5, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
fof(premise6, axiom, ( (is_a(mixture, chemical_compound) & contains_only_one_element(mixture)) | (~is_a(mixture, chemical_compound) & ~contains_only_one_element(mixture)) )).

fof(conclusion_negation, conjecture, ~(alkane(mixture) & contains_carbon(mixture))).