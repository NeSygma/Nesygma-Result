fof(publishing_house_nvp, axiom, publishing_house(new_vessel_press)).

fof(all_nvp_books_english, axiom, ! [Book] : (published_by(Book, new_vessel_press) => in_language(Book, english))).

fof(nc_published_by_nvp, axiom, published_by(neapolitan_chronicles, new_vessel_press)).

fof(nc_translated_from_italian, axiom, translated_from(neapolitan_chronicles, italian)).

fof(pof_published_by_nvp, axiom, published_by(palace_of_flies, new_vessel_press)).

fof(goal, conjecture, ~in_language(neapolitan_chronicles, english)).