% Axioms
fof(hydrocarbon_organic, axiom, ! [X] : (hydrocarbon(X) => organic(X))).
fof(alkane_hydrocarbon, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(organic_chemical, axiom, ! [X] : (organic(X) => chemical(X))).
fof(organic_contains_carbon, axiom, ! [X] : (organic(X) => contains_carbon(X))).
fof(chemical_no_single_element, axiom, ! [X] : (chemical(X) => ~single_element(X))).
fof(mixture_chemical_single_element, axiom, (chemical(mixture) & single_element(mixture)) | ( ~chemical(mixture) & ~single_element(mixture) )).
fof(goal, conjecture, contains_carbon(mixture)).