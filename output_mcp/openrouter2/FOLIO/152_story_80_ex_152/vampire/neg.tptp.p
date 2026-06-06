fof(published_neapolitan, axiom, published_by(nvp, neapolitan_chronicles)).
fof(translated_neapolitan, axiom, translated_from(neapolitan_chronicles, italian)).
fof(published_palace, axiom, published_by(nvp, palace_of_flies)).
fof(all_in_english, axiom, ! [B] : (published_by(nvp, B) => in_english(B))).
fof(distinct, axiom, (nvp != neapolitan_chronicles & nvp != palace_of_flies & neapolitan_chronicles != palace_of_flies & nvp != italian & neapolitan_chronicles != italian & palace_of_flies != italian)).
fof(conjecture, conjecture, ~translated_from(palace_of_flies, italian)).