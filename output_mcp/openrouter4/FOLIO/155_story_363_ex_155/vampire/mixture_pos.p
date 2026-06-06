fof(premise_1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(premise_2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(premise_3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(premise_4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(premise_5, axiom, ! [X] : (chemical_compound(X) => ~ contains_only_one_element(X))).
fof(premise_6, axiom, (chemical_compound(mixture) <=> contains_only_one_element(mixture))).
fof(conclusion, conjecture, (contains_only_one_element(mixture) | contains_carbon(mixture)) => (~ chemical_compound(mixture) & ~ alkane(mixture))).