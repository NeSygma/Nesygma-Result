fof(all_cats_are_mammals, axiom, ![X] : (cat(X) => mammal(X))).
fof(some_pets_not_mammals, axiom, ?[X] : (pet(X) & ~mammal(X))).
fof(conjecture, conjecture, ?[X] : (pet(X) & cat(X))).