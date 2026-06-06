fof(eastern_is_wild, axiom, ! [X] : (eastern(X) => wild_turkey(X))).
fof(osceola_is_wild, axiom, ! [X] : (osceola(X) => wild_turkey(X))).
fof(goulds_is_wild, axiom, ! [X] : (goulds(X) => wild_turkey(X))).
fof(merriams_is_wild, axiom, ! [X] : (merriams(X) => wild_turkey(X))).
fof(rio_grande_is_wild, axiom, ! [X] : (rio_grande(X) => wild_turkey(X))).
fof(ocellated_is_wild, axiom, ! [X] : (ocellated(X) => wild_turkey(X))).

fof(types_exhaustive, axiom, ! [X] : (wild_turkey(X) => (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).

fof(tom_not_eastern, axiom, ~eastern(tom)).
fof(tom_not_osceola, axiom, ~osceola(tom)).
fof(tom_not_goulds, axiom, ~goulds(tom)).
fof(tom_not_merriams, axiom, ~merriams(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande(tom)).
fof(tom_is_wild, axiom, wild_turkey(tom)).

fof(distinct_names, axiom, tom != joey).

fof(goal, conjecture, ~wild_turkey(joey)).