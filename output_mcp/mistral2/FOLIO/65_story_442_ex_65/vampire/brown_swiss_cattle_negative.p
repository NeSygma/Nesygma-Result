fof(all_brown_swiss_are_cows, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(some_pets_are_brown_swiss, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(all_cows_are_domesticated, axiom, ! [X] : (cow(X) => domesticated_animal(X))).
fof(alligators_not_domesticated, axiom, ! [X] : (alligator(X) => ~domesticated_animal(X))).
fof(ted_is_alligator, axiom, alligator(ted)).
fof(negated_conclusion_claim, conjecture, (brown_swiss_cattle(ted) & pet(ted))).