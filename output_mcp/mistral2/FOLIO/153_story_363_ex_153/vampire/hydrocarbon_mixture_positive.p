fof(all_hydrocarbons_are_organic, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(all_alkanes_are_hydrocarbons, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(all_organic_are_chemical, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(all_organic_contain_carbon, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(no_chemical_has_one_element, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
fof(mixture_property, axiom, (chemical_compound(mix) & contains_only_one_element(mix)) | (~chemical_compound(mix) & ~contains_only_one_element(mix))).
fof(goal, conjecture, contains_carbon(mix)).