fof(publishing_house_decl, axiom, publishing_house(new_vessel_press)).
fof(specializes_in_translation_decl, axiom, specializes_in_translation(new_vessel_press)).
fof(all_books_in_english, axiom,
    ! [B] : (published_by(B, new_vessel_press) => book_in_language(B, english))).
fof(neapolitan_chronicles_published, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(neapolitan_chronicles_translated, axiom, translated_from(neapolitan_chronicles, italian)).
fof(palace_of_flies_published, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(distinct_entities, axiom,
    (neapolitan_chronicles != palace_of_flies
     & neapolitan_chronicles != harry_potter
     & palace_of_flies != harry_potter)).
fof(conclusion_negation, conjecture, ~published_by(harry_potter, new_vessel_press)).