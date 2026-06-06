% Negative version: Joey is NOT a wild turkey
fof(distinct_types, axiom, (eastern != osceola & eastern != goulds & eastern != merriams & eastern != rio_grande & eastern != ocellated &
    osceola != goulds & osceola != merriams & osceola != rio_grande & osceola != ocellated &
    goulds != merriams & goulds != rio_grande & goulds != ocellated &
    merriams != rio_grande & merriams != ocellated &
    rio_grande != ocellated)).

fof(tom_not_eastern, axiom, ~type_of(tom, eastern)).
fof(tom_not_osceola, axiom, ~type_of(tom, osceola)).
fof(tom_not_goulds, axiom, ~type_of(tom, goulds)).
fof(tom_not_merriams_rio, axiom, ~type_of(tom, merriams) & ~type_of(tom, rio_grande)).
fof(tom_is_wild, axiom, wild_turkey(tom)).

fof(goal, conjecture, ~wild_turkey(joey)).