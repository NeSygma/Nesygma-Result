fof(axiom_brown_swiss_cow, axiom, ! [X] : (brown_swiss(X) => cow(X))).
fof(axiom_some_pet_brown_swiss, axiom, ? [X] : (pet(X) & brown_swiss(X))).
fof(axiom_cow_domesticated, axiom, ! [X] : (cow(X) => domesticated(X))).
fof(axiom_alligator_not_domesticated, axiom, ! [X] : (alligator(X) => ~domesticated(X))).
fof(axiom_ted_alligator, axiom, alligator(ted)).
fof(conjecture, conjecture, (brown_swiss(ted) & pet(ted))).