fof(premise_1, axiom, publishing_house(new_vessel_press)).
fof(premise_2, axiom, ! [B] : (published_by(B, new_vessel_press) => in_english(B))).
fof(premise_3, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(premise_4, axiom, translated_from(neapolitan_chronicles, italian)).
fof(premise_5, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(goal, conjecture, ~translated_from(palace_of_flies, italian)).