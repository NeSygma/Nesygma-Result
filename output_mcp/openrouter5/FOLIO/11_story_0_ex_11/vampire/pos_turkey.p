% Positive version: original claim as conjecture
% Tom is an Eastern wild turkey

% There are six types of wild turkeys
fof(type_eastern, axiom, ! [X] : (wild_turkey(X) => (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).

% Tom is a wild turkey
fof(tom_is_wild, axiom, wild_turkey(tom)).

% Tom is not an Eastern wild turkey
fof(not_eastern, axiom, ~eastern(tom)).

% Tom is not an Osceola wild turkey
fof(not_osceola, axiom, ~osceola(tom)).

% Tom is not a Gould's wild turkey
fof(not_goulds, axiom, ~goulds(tom)).

% Tom is neither a Merriam's wild turkey nor a Rio Grande wild turkey
fof(not_merriams, axiom, ~merriams(tom)).
fof(not_rio_grande, axiom, ~rio_grande(tom)).

% Conclusion: Tom is an Eastern wild turkey
fof(goal, conjecture, eastern(tom)).