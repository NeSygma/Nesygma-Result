fof(nvp_publishes_english, axiom,
    ! [X] : ((book(X) & published_by_nvp(X)) => in_english(X))).
fof(nc_is_book_nvp, axiom,
    (book(neapolitan_chronicles) & published_by_nvp(neapolitan_chronicles))).
fof(nc_translated_italian, axiom,
    translated_from_italian(neapolitan_chronicles)).
fof(pf_is_book_nvp, axiom,
    (book(palace_of_flies) & published_by_nvp(palace_of_flies))).
fof(goal, conjecture,
    translated_from_italian(palace_of_flies)).