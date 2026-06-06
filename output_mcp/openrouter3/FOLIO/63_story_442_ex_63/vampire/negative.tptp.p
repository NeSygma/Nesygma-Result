% Negative file: Premises + ~pet(ted) as conjecture
fof(brown_swiss_are_cows, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(some_pets_are_brown_swiss, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(cows_are_domesticated, axiom, ! [X] : (cow(X) => domesticated(X))).
fof(alligators_not_domesticated, axiom, ! [X] : (alligator(X) => ~domesticated(X))).
fof(ted_is_alligator, axiom, alligator(ted)).
fof(goal, conjecture, ~pet(ted)).