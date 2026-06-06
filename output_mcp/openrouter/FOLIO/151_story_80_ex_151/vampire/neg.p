% Negative test: Harry Potter not published by New Vessel Press
fof(distinct_entities, axiom, (new_vessel_press != neapolitan_chronicles & new_vessel_press != palace_of_flies & new_vessel_press != harry_potter & neapolitan_chronicles != palace_of_flies & neapolitan_chronicles != harry_potter & palace_of_flies != harry_potter)).
fof(publishing_house, axiom, publishing_house(new_vessel_press)).
fof(specializes, axiom, specializes_in(new_vessel_press, translating_foreign_literature_into_english)).
fof(all_english, axiom, ! [B] : (published(B, new_vessel_press) => in_english(B))).
fof(published_neapolitan, axiom, published(neapolitan_chronicles, new_vessel_press)).
fof(translated_neapolitan, axiom, translated_from(neapolitan_chronicles, italian)).
fof(published_palace, axiom, published(palace_of_flies, new_vessel_press)).
fof(goal, conjecture, ~published(harry_potter, new_vessel_press)).