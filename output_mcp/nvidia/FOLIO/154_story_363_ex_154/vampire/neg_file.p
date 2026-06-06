fof(all_hydrocarbon_organic, axiom, ! [X] : (hydrocarbon(X) => organic(X))).
fof(all_alkane_hydrocarbon, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(all_organic_chemical, axiom, ! [X] : (organic(X) => chemical(X))).
fof(all_organic_contains_carbon, axiom, ! [X] : (organic(X) => contains_carbon(X))).
fof(no_chemical_single_element, axiom, ! [X] : (chemical(X) => ~single_element(X))).
fof(mixture_chem_imp_single, axiom, ! [X] : (chemical(mixture) => single_element(mixture))).
fof(single_chem_imp_mixture, axiom, ! [X] : (single_element(mixture) => chemical(mixture))).
fof(neg_conclusion, conjecture, ~(alkane(mixture) & contains_carbon(mixture))).