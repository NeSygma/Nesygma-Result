% Negative version: Conjecture is "Palace of Flies was NOT translated from Italian"
fof(premise_1, axiom, ! [B] : (published_by_new_vessel_press(B) => in_english(B))).
fof(premise_2, axiom, published_by_new_vessel_press(neapolitan_chronicles)).
fof(premise_3, axiom, translated_from_italian(neapolitan_chronicles)).
fof(premise_4, axiom, published_by_new_vessel_press(palace_of_flies)).
fof(distinct, axiom, (neapolitan_chronicles != palace_of_flies)).
fof(goal, conjecture, ~translated_from_italian(palace_of_flies)).