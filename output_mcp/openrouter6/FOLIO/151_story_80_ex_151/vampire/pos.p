fof(premise1, axiom, publishing_house(new_vessel_press)).
fof(premise2, axiom, ! [X] : (published_by(X, new_vessel_press) => language(X, english))).
fof(premise3, axiom, published_by(neapolitan_chronicles, new_vessel_press)).
fof(premise4, axiom, translated_from(neapolitan_chronicles, italian)).
fof(premise5, axiom, published_by(palace_of_flies, new_vessel_press)).
fof(distinct, axiom, (new_vessel_press != neapolitan_chronicles & new_vessel_press != palace_of_flies & new_vessel_press != harry_potter & neapolitan_chronicles != palace_of_flies & neapolitan_chronicles != harry_potter & palace_of_flies != harry_potter)).
fof(goal, conjecture, published_by(harry_potter, new_vessel_press)).