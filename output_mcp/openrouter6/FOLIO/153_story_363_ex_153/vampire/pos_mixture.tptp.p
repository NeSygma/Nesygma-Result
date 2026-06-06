fof(premise1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(premise2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(premise3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(premise4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(premise5, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
fof(premise6, axiom, (chemical_compound(m) <=> contains_only_one_element(m))).
fof(goal, conjecture, contains_carbon(m)).