fof(type_eastern, axiom, (eastern = eastern)).
fof(type_osceola, axiom, (osceola = osceola)).
fof(type_goulds, axiom, (goulds = goulds)).
fof(type_merriams, axiom, (merriams = merriams)).
fof(type_rio_grande, axiom, (rio_grande = rio_grande)).
fof(type_ocellated, axiom, (ocellated = ocellated)).

fof(distinct_types, axiom, (eastern != osceola & eastern != goulds & eastern != merriams & eastern != rio_grande & eastern != ocellated &
                             osceola != goulds & osceola != merriams & osceola != rio_grande & osceola != ocellated &
                             goulds != merriams & goulds != rio_grande & goulds != ocellated &
                             merriams != rio_grande & merriams != ocellated &
                             rio_grande != ocellated)).

fof(is_wild_turkey, axiom, (wild_turkey(tom))).
fof(exhaustiveness, axiom, ! [X] : (wild_turkey(X) => (is_type(X, eastern) | is_type(X, osceola) | is_type(X, goulds) | is_type(X, merriams) | is_type(X, rio_grande) | is_type(X, ocellated)))).

fof(not_eastern, axiom, ~is_type(tom, eastern)).
fof(not_osceola, axiom, ~is_type(tom, osceola)).
fof(not_goulds, axiom, ~is_type(tom, goulds)).
fof(not_merriams, axiom, ~is_type(tom, merriams)).
fof(not_rio_grande, axiom, ~is_type(tom, rio_grande)).

fof(goal, conjecture, ~is_type(tom, ocellated)).