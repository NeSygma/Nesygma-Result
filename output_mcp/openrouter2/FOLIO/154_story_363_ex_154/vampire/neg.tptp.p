fof(all_hydrocarbons_organic, axiom, ! [X] : (hydrocarbon(X) => organic(X))).
fof(all_alkanes_hydrocarbons, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(all_organic_chemical, axiom, ! [X] : (organic(X) => chemical(X))).
fof(all_organic_carbon, axiom, ! [X] : (organic(X) => contains_carbon(X))).
fof(no_chemical_one_element, axiom, ! [X] : (chemical(X) => ~one_element(X))).
fof(chemical_one_element_equiv, axiom, chemical(mixture) => one_element(mixture)).
fof(one_element_chemical_equiv, axiom, one_element(mixture) => chemical(mixture)).
fof(goal, conjecture, ~(alkane(mixture) & contains_carbon(mixture))).