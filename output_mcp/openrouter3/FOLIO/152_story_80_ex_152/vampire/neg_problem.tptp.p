% Premises
fof(premise_1, axiom, ! [B] : (published_by(B, new_vessel_press) => translated_from(B, italian))).
fof(premise_2, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(premise_3, axiom, translated_from(neapolitan_chronicles, italian)).
fof(premise_4, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(distinct_entities, axiom, (new_vessel_press != neapolitan_chronicles & new_vessel_press != palace_of_flies & neapolitan_chronicles != palace_of_flies)).

% Negated conclusion
fof(goal, conjecture, ~translated_from(palace_of_flies, italian)).