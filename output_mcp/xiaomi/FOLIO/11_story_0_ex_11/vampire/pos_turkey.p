fof(eastern_type, axiom, ! [X] : (eastern_wild_turkey(X) => wild_turkey(X))).
fof(osceola_type, axiom, ! [X] : (osceola_wild_turkey(X) => wild_turkey(X))).
fof(goulds_type, axiom, ! [X] : (goulds_wild_turkey(X) => wild_turkey(X))).
fof(merriams_type, axiom, ! [X] : (merriams_wild_turkey(X) => wild_turkey(X))).
fof(rio_grande_type, axiom, ! [X] : (rio_grande_wild_turkey(X) => wild_turkey(X))).
fof(ocellated_type, axiom, ! [X] : (ocellated_wild_turkey(X) => wild_turkey(X))).

fof(exhaustive_types, axiom, ! [X] : (wild_turkey(X) => (eastern_wild_turkey(X) | osceola_wild_turkey(X) | goulds_wild_turkey(X) | merriams_wild_turkey(X) | rio_grande_wild_turkey(X) | ocellated_wild_turkey(X)))).

fof(tom_not_eastern, axiom, ~eastern_wild_turkey(tom)).
fof(tom_not_osceola, axiom, ~osceola_wild_turkey(tom)).
fof(tom_not_goulds, axiom, ~goulds_wild_turkey(tom)).
fof(tom_not_merriams, axiom, ~merriams_wild_turkey(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande_wild_turkey(tom)).
fof(tom_is_wild_turkey, axiom, wild_turkey(tom)).

fof(goal, conjecture, eastern_wild_turkey(tom)).