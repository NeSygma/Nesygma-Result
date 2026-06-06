fof(all_hydrocarbons_are_organic, axiom, ! [X] : (is_hydrocarbon(X) => is_organic_compound(X))).
fof(all_alkanes_are_hydrocarbons, axiom, ! [X] : (is_alkane(X) => is_hydrocarbon(X))).
fof(all_organic_are_chemical, axiom, ! [X] : (is_organic_compound(X) => is_chemical_compound(X))).
fof(all_organic_contain_carbon, axiom, ! [X] : (is_organic_compound(X) => contains_carbon(X))).
fof(no_chemical_has_one_element, axiom, ! [X] : (is_chemical_compound(X) => ~contains_only_one_element(X))).
fof(mixture_biconditional, axiom, is_mixture(m) => (is_chemical_compound(m) <=> contains_only_one_element(m))).
fof(mixture_is_mixture, axiom, is_mixture(m)).
fof(conclusion, conjecture, is_alkane(m) & contains_carbon(m)).