fof(premise1, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(premise2, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(premise3, axiom, ! [X] : (cow(X) => domesticated(X))).
fof(premise4, axiom, ! [X] : (alligator(X) => ~domesticated(X))).
fof(premise5, axiom, alligator(ted)).
fof(goal, conjecture, pet(ted) & brown_swiss_cattle(ted)).