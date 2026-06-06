% Negative version: negated claim as conjecture
% All hydrocarbons are organic compounds.
fof(hc_to_org, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
% All alkanes are hydrocarbons.
fof(alk_to_hc, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
% All organic compounds are chemical compounds.
fof(org_to_chem, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
% All organic compounds contain carbon.
fof(org_contains_carbon, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
% No chemical compounds contain only one element.
fof(no_chem_single_element, axiom, ! [X] : (chemical_compound(X) => ~contains_only_one_element(X))).
% The mixture either both is a chemical compound and contains only one element, or neither.
fof(mixture_condition, axiom, (chemical_compound(mixture) & contains_only_one_element(mixture)) | (~chemical_compound(mixture) & ~contains_only_one_element(mixture))).
% Negated conclusion: The mixture does NOT contain carbon.
fof(goal_neg, conjecture, ~contains_carbon(mixture)).