fof(nvp_publishes_english, axiom, ! [B] : (published_by(B, new_vessel_press) => is_in_english(B))).
fof(nc_published, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(pof_published, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(nc_translated, axiom, translated_from_italian(neapolitan_chronicles)).
fof(distinct_books, axiom, (neapolitan_chronicles != palace_of_flies & neapolitan_chronicles != harry_potter & palace_of_flies != harry_potter)).
fof(goal, conjecture, published_by(harry_potter, new_vessel_press)).