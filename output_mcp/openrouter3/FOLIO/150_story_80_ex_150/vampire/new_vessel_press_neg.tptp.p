% Negative version: Neapolitan Chronicles is NOT an English book
fof(new_vessel_press, axiom, publishes(new_vessel_press, neapolitan_chronicles)).
fof(all_english, axiom, ! [P, B] : (publishes(P, B) => in_english(B))).
fof(neapolitan_translated, axiom, translated_from(neapolitan_chronicles, italian)).
fof(palace_published, axiom, publishes(new_vessel_press, palace_of_flies)).
fof(goal, conjecture, ~in_english(neapolitan_chronicles)).