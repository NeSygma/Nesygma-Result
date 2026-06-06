fof(publishing_house, axiom, publishing_house(nvp)).
fof(specializes, axiom, specializes_in_translating_foreign_literature_into_english(nvp)).
fof(all_books_english, axiom, ! [B] : (published_by(B, nvp) => language(B, english))).
fof(nc_published, axiom, published_by(nc, nvp)).
fof(nc_translated, axiom, translated_from(nc, italian)).
fof(pf_published, axiom, published_by(pf, nvp)).
fof(goal, conjecture, translated_from(pf, italian)).