fof(eastern_is_wild, axiom, ! [X] : (eastern(X) => wild_turkey(X))).
fof(osceola_is_wild, axiom, ! [X] : (osceola(X) => wild_turkey(X))).
fof(goulds_is_wild, axiom, ! [X] : (goulds(X) => wild_turkey(X))).
fof(merriams_is_wild, axiom, ! [X] : (merriams(X) => wild_turkey(X))).
fof(rio_grande_is_wild, axiom, ! [X] : (rio_grande(X) => wild_turkey(X))).
fof(ocellated_is_wild, axiom, ! [X] : (ocellated(X) => wild_turkey(X))).

fof(all_wild_turkeys_are_these_types, axiom,
    ! [X] : (wild_turkey(X) <=>
             (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).

fof(mutually_exclusive_1, axiom, ! [X] : (eastern(X) => ~osceola(X))).
fof(mutually_exclusive_2, axiom, ! [X] : (eastern(X) => ~goulds(X))).
fof(mutually_exclusive_3, axiom, ! [X] : (eastern(X) => ~merriams(X))).
fof(mutually_exclusive_4, axiom, ! [X] : (eastern(X) => ~rio_grande(X))).
fof(mutually_exclusive_5, axiom, ! [X] : (eastern(X) => ~ocellated(X))).
fof(mutually_exclusive_6, axiom, ! [X] : (osceola(X) => ~goulds(X))).
fof(mutually_exclusive_7, axiom, ! [X] : (osceola(X) => ~merriams(X))).
fof(mutually_exclusive_8, axiom, ! [X] : (osceola(X) => ~rio_grande(X))).
fof(mutually_exclusive_9, axiom, ! [X] : (osceola(X) => ~ocellated(X))).
fof(mutually_exclusive_10, axiom, ! [X] : (goulds(X) => ~merriams(X))).
fof(mutually_exclusive_11, axiom, ! [X] : (goulds(X) => ~rio_grande(X))).
fof(mutually_exclusive_12, axiom, ! [X] : (goulds(X) => ~ocellated(X))).
fof(mutually_exclusive_13, axiom, ! [X] : (merriams(X) => ~rio_grande(X))).
fof(mutually_exclusive_14, axiom, ! [X] : (merriams(X) => ~ocellated(X))).
fof(mutually_exclusive_15, axiom, ! [X] : (rio_grande(X) => ~ocellated(X))).

fof(tom_not_eastern, axiom, ~eastern(tom)).
fof(tom_not_osceola, axiom, ~osceola(tom)).
fof(tom_not_goulds, axiom, ~goulds(tom)).
fof(tom_not_merriams, axiom, ~merriams(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande(tom)).
fof(tom_is_wild, axiom, wild_turkey(tom)).

fof(conclusion_negation, conjecture, ~wild_turkey(joey)).