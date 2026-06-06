% Negative test: Palace of Flies was NOT translated from Italian
fof(distinct_consts, axiom, (new_vessel_press != neapolitan_chronicles & new_vessel_press != palace_of_flies & neapolitan_chronicles != palace_of_flies)).
fof(all_english, axiom, ! [B] : (published(B, new_vessel_press) => in_english(B))).
fof(published_neapolitan, axiom, published(neapolitan_chronicles, new_vessel_press)).
fof(published_palace, axiom, published(palace_of_flies, new_vessel_press)).
fof(translated_neapolitan, axiom, translated_from(neapolitan_chronicles, italian)).
fof(goal, conjecture, ~translated_from(palace_of_flies, italian)).