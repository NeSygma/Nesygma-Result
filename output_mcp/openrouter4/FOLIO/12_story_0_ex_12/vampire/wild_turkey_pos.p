% Positive test: is "Joey is a wild turkey" entailed?
% Six types of wild turkeys
fof(type_eastern, axiom, ! [X] : (eastern(X) => wild_turkey(X))).
fof(type_osceola, axiom, ! [X] : (osceola(X) => wild_turkey(X))).
fof(type_goulds, axiom, ! [X] : (goulds(X) => wild_turkey(X))).
fof(type_merriams, axiom, ! [X] : (merriams(X) => wild_turkey(X))).
fof(type_rio_grande, axiom, ! [X] : (rio_grande(X) => wild_turkey(X))).
fof(type_ocellated, axiom, ! [X] : (ocellated(X) => wild_turkey(X))).

% Every wild turkey belongs to one of the six types
fof(wild_turkey_covered, axiom, ! [X] : (wild_turkey(X) =>
    (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).

% The six types are mutually exclusive (a bird is exactly one type)
fof(mutual_excl_1, axiom, ! [X] : (eastern(X) => ~osceola(X))).
fof(mutual_excl_2, axiom, ! [X] : (eastern(X) => ~goulds(X))).
fof(mutual_excl_3, axiom, ! [X] : (eastern(X) => ~merriams(X))).
fof(mutual_excl_4, axiom, ! [X] : (eastern(X) => ~rio_grande(X))).
fof(mutual_excl_5, axiom, ! [X] : (eastern(X) => ~ocellated(X))).
fof(mutual_excl_6, axiom, ! [X] : (osceola(X) => ~goulds(X))).
fof(mutual_excl_7, axiom, ! [X] : (osceola(X) => ~merriams(X))).
fof(mutual_excl_8, axiom, ! [X] : (osceola(X) => ~rio_grande(X))).
fof(mutual_excl_9, axiom, ! [X] : (osceola(X) => ~ocellated(X))).
fof(mutual_excl_10, axiom, ! [X] : (goulds(X) => ~merriams(X))).
fof(mutual_excl_11, axiom, ! [X] : (goulds(X) => ~rio_grande(X))).
fof(mutual_excl_12, axiom, ! [X] : (goulds(X) => ~ocellated(X))).
fof(mutual_excl_13, axiom, ! [X] : (merriams(X) => ~rio_grande(X))).
fof(mutual_excl_14, axiom, ! [X] : (merriams(X) => ~ocellated(X))).
fof(mutual_excl_15, axiom, ! [X] : (rio_grande(X) => ~ocellated(X))).

% Facts about Tom
fof(tom_not_eastern, axiom, ~eastern(tom)).
fof(tom_not_osceola, axiom, ~osceola(tom)).
fof(tom_not_goulds, axiom, ~goulds(tom)).
fof(tom_not_merriams, axiom, ~merriams(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande(tom)).
fof(tom_is_wild_turkey, axiom, wild_turkey(tom)).

% Conclusion: Joey is a wild turkey
fof(conclusion, conjecture, wild_turkey(joey)).