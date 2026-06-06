fof(distinct_types, axiom, (eastern != osceola & eastern != goulds & eastern != merriams & eastern != rio_grande & eastern != ocellated & osceola != goulds & osceola != merriams & osceola != rio_grande & osceola != ocellated & goulds != merriams & goulds != rio_grande & goulds != ocellated & merriams != rio_grande & merriams != ocellated & rio_grande != ocellated)).
fof(distinct_tom, axiom, (tom != eastern & tom != osceola & tom != goulds & tom != merriams & tom != rio_grande & tom != ocellated)).
fof(tom_wild_turkey, axiom, wild_turkey(tom)).
fof(not_eastern, axiom, ~is_of_type(tom, eastern)).
fof(not_osceola, axiom, ~is_of_type(tom, osceola)).
fof(not_goulds, axiom, ~is_of_type(tom, goulds)).
fof(not_merriams, axiom, ~is_of_type(tom, merriams)).
fof(not_rio_grande, axiom, ~is_of_type(tom, rio_grande)).
fof(goal, conjecture, ~is_of_type(tom, ocellated)).