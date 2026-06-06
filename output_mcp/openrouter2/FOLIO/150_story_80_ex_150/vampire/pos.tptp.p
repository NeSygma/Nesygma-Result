fof(publishing_house, axiom, publishing_house(new_vessel_press)).
fof(specializes, axiom, specializes_in_translation_to_english(new_vessel_press)).
fof(all_in_english, axiom, ! [B] : ((published_by(B, new_vessel_press)) => in_english(B))).
fof(published_neapolitan, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(translated_from, axiom, translated_from(neapolitan_chronicles, italian)).
fof(published_palace, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(distinct, axiom, (new_vessel_press != neapolitan_chronicles & new_vessel_press != palace_of_flies & neapolitan_chronicles != palace_of_flies)).
fof(goal, conjecture, in_english(neapolitan_chronicles)).