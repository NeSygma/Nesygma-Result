fof(all_types, axiom,
    ( wild_turkey_type(eastern)
    & wild_turkey_type(osceola)
    & wild_turkey_type(gould)
    & wild_turkey_type(merriam)
    & wild_turkey_type(rio_grande)
    & wild_turkey_type(ocellated) )).

fof(tom_not_eastern, axiom, ~is_tom_type(eastern)).
fof(tom_not_osceola, axiom, ~is_tom_type(osceola)).
fof(tom_not_gould, axiom, ~is_tom_type(gould)).
fof(tom_not_merriam_or_rio, axiom, (~is_tom_type(merriam) & ~is_tom_type(rio_grande))).

fof(tom_is_wild_turkey, axiom, wild_turkey(tom)).

fof(goal, conjecture, wild_turkey(joey)).