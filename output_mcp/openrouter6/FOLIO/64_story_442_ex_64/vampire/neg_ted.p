fof(brown_swiss_are_cows, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(some_pets_are_bsc, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(cows_are_domesticated, axiom, ! [X] : (cow(X) => domesticated_animal(X))).
fof(alligators_not_domesticated, axiom, ! [X] : (alligator(X) => ~domesticated_animal(X))).
fof(ted_is_alligator, axiom, alligator(ted)).
fof(goal_neg, conjecture, ~(pet(ted) & brown_swiss_cattle(ted))).