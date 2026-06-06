% Positive test: Tom is an Ocellated wild turkey
fof(exhaustive_types, axiom,
    ! [X] : (wild_turkey(X) =>
        (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).
fof(not_eastern, axiom, ~eastern(tom)).
fof(not_osceola, axiom, ~osceola(tom)).
fof(not_goulds, axiom, ~goulds(tom)).
fof(not_merriams, axiom, ~merriams(tom)).
fof(not_rio_grande, axiom, ~rio_grande(tom)).
fof(tom_is_wild, axiom, wild_turkey(tom)).
fof(goal, conjecture, ocellated(tom)).