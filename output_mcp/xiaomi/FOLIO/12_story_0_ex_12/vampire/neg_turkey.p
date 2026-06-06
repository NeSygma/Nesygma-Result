fof(turkey_types, axiom, ! [X] : (wild_turkey(X) => 
    (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).

fof(distinct_types, axiom, (
    eastern != osceola & eastern != goulds & eastern != merriams & eastern != rio_grande & eastern != ocellated &
    osceola != goulds & osceola != merriams & osceola != rio_grande & osceola != ocellated &
    goulds != merriams & goulds != rio_grande & goulds != ocellated &
    merriams != rio_grande & merriams != ocellated &
    rio_grande != ocellated
)).

fof(tom_not_eastern, axiom, ~eastern(tom)).
fof(tom_not_osceola, axiom, ~osceola(tom)).
fof(tom_not_goulds, axiom, ~goulds(tom)).
fof(tom_not_merriams, axiom, ~merriams(tom)).
fof(tom_not_rio_grande, axiom, ~rio_grande(tom)).
fof(tom_is_wild_turkey, axiom, wild_turkey(tom)).

fof(goal, conjecture, ~wild_turkey(joey)).