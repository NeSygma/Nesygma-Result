fof(premise_all_english, axiom,
    ! [B] : (publishes(new_vessel_press, B) => in_english(B))).
fof(premise_nc_published, axiom,
    publishes(new_vessel_press, neapolitan_chronicles)).
fof(premise_nc_translated, axiom,
    translated_from(neapolitan_chronicles, italian)).
fof(premise_pof_published, axiom,
    publishes(new_vessel_press, palace_of_flies)).
fof(goal, conjecture,
    in_english(neapolitan_chronicles)).