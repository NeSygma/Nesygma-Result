% Axioms
fof(specialization, axiom, ! [X] : (published_by(new_vessel_press, X) => translated_from_foreign_into_English(X))).
fof(all_published_english, axiom, ! [X] : (published_by(new_vessel_press, X) => in_English(X))).
fof(fact_nc_published, axiom, published_by(new_vessel_press, neapolitan_chronicles)).
fof(fact_nc_translated_from_italian, axiom, translated_from_Italian(neapolitan_chronicles)).
fof(fact_palace_published, axiom, published_by(new_vessel_press, palace_of_flies)).
fof(distinct_constants, axiom, (new_vessel_press != neapolitan_chronicles & new_vessel_press != palace_of_flies & new_vessel_press != harry_potter & neapolitan_chronicles != palace_of_flies & neapolitan_chronicles != harry_potter & palace_of_flies != harry_potter)).
fof(goal, conjecture, ~published_by(new_vessel_press, harry_potter)).