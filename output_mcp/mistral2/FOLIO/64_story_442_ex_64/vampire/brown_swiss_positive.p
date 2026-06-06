fof(all_brown_swiss_are_cows, axiom, ! [X] : (is_brown_swiss_cattle(X) => is_cow(X))).
fof(some_pets_are_brown_swiss, axiom, ? [X] : (is_pet(X) & is_brown_swiss_cattle(X))).
fof(all_cows_are_domesticated, axiom, ! [X] : (is_cow(X) => is_domesticated(X))).
fof(alligators_not_domesticated, axiom, ! [X] : (is_alligator(X) => ~is_domesticated(X))).
fof(ted_is_alligator, axiom, is_alligator(ted)).
fof(conclusion, conjecture, is_pet(ted) & is_brown_swiss_cattle(ted)).