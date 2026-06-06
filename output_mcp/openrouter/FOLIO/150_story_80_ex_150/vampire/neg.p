% Negative version
fof(distinct_consts, axiom, (neapolitan_chronicles != palace_of_flies & neapolitan_chronicles != new_vessel_press & palace_of_flies != new_vessel_press)).
fof(published_neapolitan, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(published_palace, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(all_english, axiom, ![B] : (published_by(B, new_vessel_press) => english(B))).
fof(translated_neapolitan, axiom, translated_from(neapolitan_chronicles, italian)).
fof(goal, conjecture, ~english(neapolitan_chronicles)).