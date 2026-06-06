fof(all_bsc_are_cows, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(some_pets_are_bsc, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(all_cows_are_domestic, axiom, ! [X] : (cow(X) => domesticated_animal(X))).
fof(alligators_not_domestic, axiom, ! [X] : (alligator(X) => ~domesticated_animal(X))).
fof(ted_is_alligator, axiom, alligator(ted)).
fof(goal, conjecture, brown_swiss_cattle(ted) => ~pet(ted)).