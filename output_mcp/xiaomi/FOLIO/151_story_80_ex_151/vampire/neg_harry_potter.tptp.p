fof(publishing_house, axiom, publisher(new_vessel_press)).
fof(premise_1, axiom, ! [B] : (published_by(B, new_vessel_press) => in_english(B))).
fof(premise_2, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(premise_3, axiom, translated_from(neapolitan_chronicles, italian)).
fof(premise_4, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(harry_potter_exists, axiom, book(harry_potter)).
fof(goal, conjecture, ~published_by(harry_potter, new_vessel_press)).