fof(publishing_house_decl, axiom, new_vessel_press_is_a_publishing_house).
fof(book_decl, axiom, neapolitan_chronicles_is_a_book).
fof(book_decl2, axiom, palace_of_flies_is_a_book).
fof(language_decl, axiom, italian_is_a_language).
fof(language_decl2, axiom, english_is_a_language).

fof(new_vessel_press_specializes_in_english, axiom, specializes_in(new_vessel_press, english)).
fof(all_new_vessel_books_are_in_english, axiom, ! [B] : (published_by(B, new_vessel_press) => book_in_language(B, english))).
fof(neapolitan_chronicles_published_by_nvp, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(neapolitan_chronicles_translated_from_italian, axiom, translated_from(neapolitan_chronicles, italian)).
fof(palace_of_flies_published_by_nvp, axiom, published_by(palace_of_flies, new_vessel_press)).

fof(distinct_books, axiom, neapolitan_chronicles != palace_of_flies).
fof(distinct_languages, axiom, italian != english).

fof(conclusion_negation, conjecture, ~translated_from(palace_of_flies, italian)).