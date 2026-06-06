fof(tom_not_eastern, axiom, ~is_tom_type(eastern)).
fof(tom_not_osceola, axiom, ~is_tom_type(osceola)).
fof(tom_not_goulds, axiom, ~is_tom_type(goulds)).
fof(tom_not_merriams, axiom, ~is_tom_type(merriams)).
fof(tom_not_riogrande, axiom, ~is_tom_type(riogrande)).
fof(tom_is_wild_turkey, axiom, is_tom_type(eastern) | is_tom_type(osceola) | is_tom_type(goulds) | is_tom_type(merriams) | is_tom_type(riogrande) | is_tom_type(ocellated)).
fof(conclusion_negation, conjecture, ~is_tom_type(eastern)).