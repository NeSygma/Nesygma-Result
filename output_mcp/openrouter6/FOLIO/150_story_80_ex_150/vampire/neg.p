fof(premise_1, axiom, publishing_house(new_vessel_press) & specializes_in_translating(new_vessel_press)).
fof(premise_2, axiom, ! [B] : (published_by(B, new_vessel_press) => in_english(B))).
fof(premise_3, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(premise_4, axiom, translated_from(neapolitan_chronicles, italian)).
fof(premise_5, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(distinctness, axiom, (new_vessel_press != neapolitan_chronicles & new_vessel_press != palace_of_flies & neapolitan_chronicles != palace_of_flies)).
fof(goal, conjecture, ~in_english(neapolitan_chronicles)).