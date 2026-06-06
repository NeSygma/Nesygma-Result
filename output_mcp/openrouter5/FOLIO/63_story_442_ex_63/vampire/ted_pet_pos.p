% Positive version: claim "Ted is a pet" as conjecture
fof(premise_1, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(premise_2, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(premise_3, axiom, ! [X] : (cow(X) => domesticated_animal(X))).
fof(premise_4, axiom, ! [X] : (alligator(X) => ~domesticated_animal(X))).
fof(premise_5, axiom, alligator(ted)).
fof(goal, conjecture, pet(ted)).