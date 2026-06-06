fof(publisher_is_new_vessel_press, axiom, publisher(new_vessel_press)).
fof(all_new_vessel_books_are_english, axiom, ! [B] : (published_by(B, new_vessel_press) => is_english(B))).
fof(neapolitan_chronicles_is_a_book, axiom, book(neapolitan_chronicles)).
fof(palace_of_flies_is_a_book, axiom, book(palace_of_flies)).
fof(neapolitan_chronicles_published_by_new_vessel, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(palace_of_flies_published_by_new_vessel, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(goal_negation, conjecture, ~is_english(neapolitan_chronicles)).