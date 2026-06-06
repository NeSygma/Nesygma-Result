fof(publishing_house_nvp, axiom, publishing_house(nvp)).
fof(all_published_in_english, axiom, ! [X] : (published(X, nvp) => in_english(X))).
fof(published_neapolitan, axiom, published(neapolitan_chronicles, nvp)).
fof(translated_from_neapolitan, axiom, translated_from(neapolitan_chronicles, italian)).
fof(published_palace, axiom, published(palace_of_flies, nvp)).
fof(distinct_constants, axiom, (nvp != neapolitan_chronicles & nvp != palace_of_flies & nvp != harry_potter & neapolitan_chronicles != palace_of_flies & neapolitan_chronicles != harry_potter & palace_of_flies != harry_potter & italian != english)).
fof(goal, conjecture, published(harry_potter, nvp)).