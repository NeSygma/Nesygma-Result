% Positive version: original claim as conjecture
% Tom is a wild turkey, and we want to check if Joey is a wild turkey.

% There are six types of wild turkeys
fof(type_eastern, axiom, ! [X] : (eastern_wild_turkey(X) => wild_turkey(X))).
fof(type_osceola, axiom, ! [X] : (osceola_wild_turkey(X) => wild_turkey(X))).
fof(type_goulds, axiom, ! [X] : (goulds_wild_turkey(X) => wild_turkey(X))).
fof(type_merriams, axiom, ! [X] : (merriams_wild_turkey(X) => wild_turkey(X))).
fof(type_rio_grande, axiom, ! [X] : (rio_grande_wild_turkey(X) => wild_turkey(X))).
fof(type_ocellated, axiom, ! [X] : (ocellated_wild_turkey(X) => wild_turkey(X))).

% Tom is not an Eastern wild turkey
fof(not_eastern, axiom, ~eastern_wild_turkey(tom)).
% Tom is not an Osceola wild turkey
fof(not_osceola, axiom, ~osceola_wild_turkey(tom)).
% Tom is not a Gould's wild turkey
fof(not_goulds, axiom, ~goulds_wild_turkey(tom)).
% Tom is neither a Merriam's wild turkey nor a Rio Grande wild turkey
fof(not_merriams, axiom, ~merriams_wild_turkey(tom)).
fof(not_rio_grande, axiom, ~rio_grande_wild_turkey(tom)).
% Tom is a wild turkey
fof(tom_wild, axiom, wild_turkey(tom)).

% Conclusion: Joey is a wild turkey
fof(conclusion, conjecture, wild_turkey(joey)).