fof(hydrocarbon_imp_organic, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(alkane_imp_hydrocarbon, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(organic_imp_chemical, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(organic_contains_carbon, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(no_chemical_one_element, axiom, ! [X] : (chemical_compound(X) => ~only_one_element(X))).
fof(premise6, axiom, (chemical_compound(mixture) & only_one_element(mixture)) | (~chemical_compound(mixture) & ~only_one_element(mixture)).
fof(conclusion, conjecture, (only_one_element(mixture) | contains_carbon(mixture)) => (~chemical_compound(mixture) & ~alkane(mixture)).