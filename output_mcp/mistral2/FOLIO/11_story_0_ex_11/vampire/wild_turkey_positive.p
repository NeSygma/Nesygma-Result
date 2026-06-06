fof(all_types_are_distinct, axiom,
    ! [X] : (
        (eastern_wild_turkey(X) => ~osceola_wild_turkey(X)) &
        (eastern_wild_turkey(X) => ~goulds_wild_turkey(X)) &
        (eastern_wild_turkey(X) => ~merriams_wild_turkey(X)) &
        (eastern_wild_turkey(X) => ~rio_grande_wild_turkey(X)) &
        (eastern_wild_turkey(X) => ~ocellated_wild_turkey(X)) &
        (osceola_wild_turkey(X) => ~goulds_wild_turkey(X)) &
        (osceola_wild_turkey(X) => ~merriams_wild_turkey(X)) &
        (osceola_wild_turkey(X) => ~rio_grande_wild_turkey(X)) &
        (osceola_wild_turkey(X) => ~ocellated_wild_turkey(X)) &
        (goulds_wild_turkey(X) => ~merriams_wild_turkey(X)) &
        (goulds_wild_turkey(X) => ~rio_grande_wild_turkey(X)) &
        (goulds_wild_turkey(X) => ~ocellated_wild_turkey(X)) &
        (merriams_wild_turkey(X) => ~rio_grande_wild_turkey(X)) &
        (merriams_wild_turkey(X) => ~ocellated_wild_turkey(X)) &
        (rio_grande_wild_turkey(X) => ~ocellated_wild_turkey(X))
    )).

fof(tom_not_eastern, axiom, ~eastern_wild_turkey(tom)).
fof(tom_not_osceola, axiom, ~osceola_wild_turkey(tom)).
fof(tom_not_goulds, axiom, ~goulds_wild_turkey(tom)).
fof(tom_not_merriams, axiom, ~merriams_wild_turkey(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande_wild_turkey(tom)).
fof(tom_is_wild_turkey, axiom, wild_turkey(tom)).

fof(goal, conjecture, eastern_wild_turkey(tom)).