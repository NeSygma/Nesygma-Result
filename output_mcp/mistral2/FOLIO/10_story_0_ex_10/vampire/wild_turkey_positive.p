tff(eastern_wild_turkey_type, type, eastern_wild_turkey: $tType).
tff(osceola_wild_turkey_type, type, osceola_wild_turkey: $tType).
tff(goulds_wild_turkey_type, type, goulds_wild_turkey: $tType).
tff(merriams_wild_turkey_type, type, merriams_wild_turkey: $tType).
tff(rio_grande_wild_turkey_type, type, rio_grande_wild_turkey: $tType).
tff(ocellated_wild_turkey_type, type, ocellated_wild_turkey: $tType).
tff(tom_type, type, tom: $tType).

tff(eastern_wild_turkey_def, axiom, eastern_wild_turkey = eastern_wild_turkey).
tff(osceola_wild_turkey_def, axiom, osceola_wild_turkey = osceola_wild_turkey).
tff(goulds_wild_turkey_def, axiom, goulds_wild_turkey = goulds_wild_turkey).
tff(merriams_wild_turkey_def, axiom, merriams_wild_turkey = merriams_wild_turkey).
tff(rio_grande_wild_turkey_def, axiom, rio_grande_wild_turkey = rio_grande_wild_turkey).
tff(ocellated_wild_turkey_def, axiom, ocellated_wild_turkey = ocellated_wild_turkey).

tff(tom_not_eastern, axiom, tom != eastern_wild_turkey).
tff(tom_not_osceola, axiom, tom != osceola_wild_turkey).
tff(tom_not_goulds, axiom, tom != goulds_wild_turkey).
tff(tom_not_merriams, axiom, tom != merriams_wild_turkey).
tff(tom_not_rio_grande, axiom, tom != rio_grande_wild_turkey).

tff(tom_is_wild_turkey, axiom, tom = eastern_wild_turkey | tom = osceola_wild_turkey | tom = goulds_wild_turkey | tom = merriams_wild_turkey | tom = rio_grande_wild_turkey | tom = ocellated_wild_turkey).

tff(conclusion, conjecture, tom = ocellated_wild_turkey).