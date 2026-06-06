% Positive file: Testing if Tom is Ocellated wild turkey
fof(tom_is_wild_turkey, axiom, wild_turkey(tom)).
fof(eastern_type, axiom, ! [X] : (eastern_wild_turkey(X) => wild_turkey(X))).
fof(osceola_type, axiom, ! [X] : (osceola_wild_turkey(X) => wild_turkey(X))).
fof(goulds_type, axiom, ! [X] : (goulds_wild_turkey(X) => wild_turkey(X))).
fof(merriams_type, axiom, ! [X] : (merriams_wild_turkey(X) => wild_turkey(X))).
fof(rio_grande_type, axiom, ! [X] : (rio_grande_wild_turkey(X) => wild_turkey(X))).
fof(oceallated_type, axiom, ! [X] : (oceallated_wild_turkey(X) => wild_turkey(X))).

% Mutually exclusive: each wild turkey is exactly one type
fof(exclusive_eastern, axiom, ! [X] : (eastern_wild_turkey(X) => ~(osceola_wild_turkey(X) | goulds_wild_turkey(X) | merriams_wild_turkey(X) | rio_grande_wild_turkey(X) | oceallated_wild_turkey(X)))).
fof(exclusive_osceola, axiom, ! [X] : (osceola_wild_turkey(X) => ~(eastern_wild_turkey(X) | goulds_wild_turkey(X) | merriams_wild_turkey(X) | rio_grande_wild_turkey(X) | oceallated_wild_turkey(X)))).
fof(exclusive_goulds, axiom, ! [X] : (goulds_wild_turkey(X) => ~(eastern_wild_turkey(X) | osceola_wild_turkey(X) | merriams_wild_turkey(X) | rio_grande_wild_turkey(X) | oceallated_wild_turkey(X)))).
fof(exclusive_merriams, axiom, ! [X] : (merriams_wild_turkey(X) => ~(eastern_wild_turkey(X) | osceola_wild_turkey(X) | goulds_wild_turkey(X) | rio_grande_wild_turkey(X) | oceallated_wild_turkey(X)))).
fof(exclusive_rio_grande, axiom, ! [X] : (rio_grande_wild_turkey(X) => ~(eastern_wild_turkey(X) | osceola_wild_turkey(X) | goulds_wild_turkey(X) | merriams_wild_turkey(X) | oceallated_wild_turkey(X)))).
fof(exclusive_oceallated, axiom, ! [X] : (oceallated_wild_turkey(X) => ~(eastern_wild_turkey(X) | osceola_wild_turkey(X) | goulds_wild_turkey(X) | merriams_wild_turkey(X) | rio_grande_wild_turkey(X)))).

% Tom is not each of the 5 non-Ocellated types
fof(tom_not_eastern, axiom, ~eastern_wild_turkey(tom)).
fof(tom_not_osceola, axiom, ~osceola_wild_turkey(tom)).
fof(tom_not_goulds, axiom, ~goulds_wild_turkey(tom)).
fof(tom_not_merriams, axiom, ~merriams_wild_turkey(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande_wild_turkey(tom)).

% Conclusion to test
fof(goal, conjecture, oceallated_wild_turkey(tom)).