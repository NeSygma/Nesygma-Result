% Negative version: claim that Neapolitan Chronicles is NOT in English
fof(all_nvp_books_english, axiom, ! [X] : (nvp_book(X) => in_english(X))).
fof(nc_is_nvp_book, axiom, nvp_book(neapolitan_chronicles)).
fof(goal_negated, conjecture, ~in_english(neapolitan_chronicles)).