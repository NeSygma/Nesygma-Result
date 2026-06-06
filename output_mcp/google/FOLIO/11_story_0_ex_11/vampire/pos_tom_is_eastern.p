fof(type_eastern, axiom, ~is_type(tom, eastern)).
fof(type_osceola, axiom, ~is_type(tom, osceola)).
fof(type_goulds, axiom, ~is_type(tom, goulds)).
fof(type_merriams, axiom, ~is_type(tom, merriams)).
fof(type_rio_grande, axiom, ~is_type(tom, rio_grande)).
fof(tom_is_wild_turkey, axiom, is_wild_turkey(tom)).
fof(wild_turkey_definition, axiom, ! [X] : (is_wild_turkey(X) <=> (is_type(X, eastern) | is_type(X, osceola) | is_type(X, goulds) | is_type(X, merriams) | is_type(X, rio_grande) | is_type(X, ocellated)))).
fof(goal, conjecture, is_type(tom, eastern)).