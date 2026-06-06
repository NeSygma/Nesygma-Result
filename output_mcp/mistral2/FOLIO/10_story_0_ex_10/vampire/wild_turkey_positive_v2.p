fof(eastern_wild_turkey, axiom, wild_turkey_type(eastern_wild_turkey)).
fof(osceola_wild_turkey, axiom, wild_turkey_type(osceola_wild_turkey)).
fof(goulds_wild_turkey, axiom, wild_turkey_type(goulds_wild_turkey)).
fof(merriams_wild_turkey, axiom, wild_turkey_type(merriams_wild_turkey)).
fof(rio_grande_wild_turkey, axiom, wild_turkey_type(rio_grande_wild_turkey)).
fof(ocellated_wild_turkey, axiom, wild_turkey_type(ocellated_wild_turkey)).

fof(tom_not_eastern, axiom, tom != eastern_wild_turkey).
fof(tom_not_osceola, axiom, tom != osceola_wild_turkey).
fof(tom_not_goulds, axiom, tom != goulds_wild_turkey).
fof(tom_not_merriams, axiom, tom != merriams_wild_turkey).
fof(tom_not_rio_grande, axiom, tom != rio_grande_wild_turkey).

fof(tom_is_wild_turkey, axiom, wild_turkey_type(tom)).

fof(domain_closure, axiom, 
    tom = eastern_wild_turkey | tom = osceola_wild_turkey | tom = goulds_wild_turkey | 
    tom = merriams_wild_turkey | tom = rio_grande_wild_turkey | tom = ocellated_wild_turkey).

fof(conclusion, conjecture, tom = ocellated_wild_turkey).