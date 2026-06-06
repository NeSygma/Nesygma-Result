% Positive file: original claim as conjecture
fof(premise_exhaustive, axiom,
    ! [X] : (wild_turkey(X) =>
        (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).
fof(premise_not_eastern, axiom, ~eastern(tom)).
fof(premise_not_osceola, axiom, ~osceola(tom)).
fof(premise_not_goulds, axiom, ~goulds(tom)).
fof(premise_not_merriams_nor_rio, axiom, (~merriams(tom) & ~rio_grande(tom))).
fof(premise_wild_turkey, axiom, wild_turkey(tom)).
fof(conclusion, conjecture, eastern(tom)).