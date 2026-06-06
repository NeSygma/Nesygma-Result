fof(publisher_specializes, axiom, specializes_in(new_vessel_press, english)).
fof(all_books_in_english, axiom, ! [B] : (published_by(B, new_vessel_press) => in_language(B, english))).
fof(neapolitan_published, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(neapolitan_translated, axiom, translated_from(neapolitan_chronicles, italian)).
fof(palace_published, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(conclusion_negation, conjecture, ~translated_from(palace_of_flies, italian)).