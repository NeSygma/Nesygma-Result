fof(type_def, axiom, ! [X] : (is_wild_turkey(X) <=> (is_eastern(X) | is_osceola(X) | is_goulds(X) | is_merriams(X) | is_rio_grande(X) | is_ocellated(X)))).
fof(tom_is_wild, axiom, is_wild_turkey(tom)).
fof(tom_not_eastern, axiom, ~is_eastern(tom)).
fof(tom_not_osceola, axiom, ~is_osceola(tom)).
fof(tom_not_goulds, axiom, ~is_goulds(tom)).
fof(tom_not_merriams, axiom, ~is_merriams(tom)).
fof(tom_not_rio_grande, axiom, ~is_rio_grande(tom)).
fof(goal, conjecture, is_wild_turkey(joey)).