fof(tom_is_one_of_six, axiom, eastern_wild_turkey(tom) | osceola_wild_turkey(tom) | goulds_wild_turkey(tom) | merriams_wild_turkey(tom) | rio_grande_wild_turkey(tom) | ocellated_wild_turkey(tom)).
fof(tom_not_eastern, axiom, ~eastern_wild_turkey(tom)).
fof(tom_not_osceola, axiom, ~osceola_wild_turkey(tom)).
fof(tom_not_goulds, axiom, ~goulds_wild_turkey(tom)).
fof(tom_not_merriam_or_rio, axiom, (~merriams_wild_turkey(tom) & ~rio_grande_wild_turkey(tom))).
fof(conclusion_negation, conjecture, ~ocellated_wild_turkey(tom)).