fof(all_brown_swift_cattle_are_cows, axiom, ![X] : (brown_swift_cattle(X) => cow(X))).
fof(some_pets_are_brown_swift_cattle, axiom, ?[X] : (pet(X) & brown_swift_cattle(X))).
fof(all_cows_are_domesticated, axiom, ![X] : (cow(X) => domesticated(X))).
fof(alligators_not_domesticated, axiom, ![X] : (alligator(X) => ~domesticated(X))).
fof(ted_is_alligator, axiom, alligator(ted)).
fof(conjecture, conjecture, ~pet(ted)).