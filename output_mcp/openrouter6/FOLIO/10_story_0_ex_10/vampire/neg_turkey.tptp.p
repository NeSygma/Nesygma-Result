% Negative TPTP file: Tom is NOT an Ocellated wild turkey
fof(type_eastern, axiom, ! [X] : (eastern(X) => wild_turkey(X))).
fof(type_osceola, axiom, ! [X] : (osceola(X) => wild_turkey(X))).
fof(type_goulds, axiom, ! [X] : (goulds(X) => wild_turkey(X))).
fof(type_merriams, axiom, ! [X] : (merriams(X) => wild_turkey(X))).
fof(type_rio_grande, axiom, ! [X] : (rio_grande(X) => wild_turkey(X))).
fof(type_ocellated, axiom, ! [X] : (ocellated(X) => wild_turkey(X))).

% Mutual exclusivity: no turkey can be two different types
fof(excl_eastern_osceola, axiom, ! [X] : ~(eastern(X) & osceola(X))).
fof(excl_eastern_goulds, axiom, ! [X] : ~(eastern(X) & goulds(X))).
fof(excl_eastern_merriams, axiom, ! [X] : ~(eastern(X) & merriams(X))).
fof(excl_eastern_rio_grande, axiom, ! [X] : ~(eastern(X) & rio_grande(X))).
fof(excl_eastern_ocellated, axiom, ! [X] : ~(eastern(X) & ocellated(X))).
fof(excl_osceola_goulds, axiom, ! [X] : ~(osceola(X) & goulds(X))).
fof(excl_osceola_merriams, axiom, ! [X] : ~(osceola(X) & merriams(X))).
fof(excl_osceola_rio_grande, axiom, ! [X] : ~(osceola(X) & rio_grande(X))).
fof(excl_osceola_ocellated, axiom, ! [X] : ~(osceola(X) & ocellated(X))).
fof(excl_goulds_merriams, axiom, ! [X] : ~(goulds(X) & merriams(X))).
fof(excl_goulds_rio_grande, axiom, ! [X] : ~(goulds(X) & rio_grande(X))).
fof(excl_goulds_ocellated, axiom, ! [X] : ~(goulds(X) & ocellated(X))).
fof(excl_merriams_rio_grande, axiom, ! [X] : ~(merriams(X) & rio_grande(X))).
fof(excl_merriams_ocellated, axiom, ! [X] : ~(merriams(X) & ocellated(X))).
fof(excl_rio_grande_ocellated, axiom, ! [X] : ~(rio_grande(X) & ocellated(X))).

% Exhaustiveness: every wild turkey is one of the six types
fof(exhaustive, axiom, ! [X] : (wild_turkey(X) => (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).

% Premises about Tom
fof(tom_wild_turkey, axiom, wild_turkey(tom)).
fof(tom_not_eastern, axiom, ~eastern(tom)).
fof(tom_not_osceola, axiom, ~osceola(tom)).
fof(tom_not_goulds, axiom, ~goulds(tom)).
fof(tom_not_merriams, axiom, ~merriams(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande(tom)).

% Negated conclusion: Tom is NOT an Ocellated wild turkey
fof(goal, conjecture, ~ocellated(tom)).