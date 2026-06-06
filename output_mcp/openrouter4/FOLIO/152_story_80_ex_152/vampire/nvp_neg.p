% Negative version: Check if Palace of Flies was NOT translated from Italian
fof(all_in_english, axiom, ! [X] : (published_by(X, new_vessel_press) => in_language(X, english))).
fof(nc_published, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(nc_translated, axiom, translated_from(neapolitan_chronicles, italian)).
fof(pf_published, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(goal, conjecture, ~translated_from(palace_of_flies, italian)).