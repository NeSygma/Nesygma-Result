fof(premise_1, axiom, ! [X] : (brown_swiss(X) => cow(X))).
fof(premise_2, axiom, ? [X] : (pet(X) & brown_swiss(X))).
fof(premise_3, axiom, ! [X] : (cow(X) => domesticated(X))).
fof(premise_4, axiom, ! [X] : (alligator(X) => ~domesticated(X))).
fof(premise_5, axiom, alligator(ted)).
fof(goal, conjecture, ~(pet(ted) & brown_swiss(ted))).