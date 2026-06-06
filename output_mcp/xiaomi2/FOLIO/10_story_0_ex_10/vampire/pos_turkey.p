fof(types_exhaustive, axiom, ! [X] : (wild_turkey(X) =>
    (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).
fof(tom_not_eastern, axiom, ~eastern(tom)).
fof(tom_not_osceola, axiom, ~osceola(tom)).
fof(tom_not_goulds, axiom, ~goulds(tom)).
fof(tom_not_merriams, axiom, ~merriams(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande(tom)).
fof(tom_is_wild_turkey, axiom, wild_turkey(tom)).
fof(goal, conjecture, ocellated(tom)).