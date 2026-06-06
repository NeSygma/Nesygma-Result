fof(all_cats_mammals, axiom, ! [X] : (cat(X) => mammal(X))).
fof(some_pets_not_mammals, axiom, ? [X] : (pet(X) & ~mammal(X))).
fof(goal, conjecture, ? [X] : (pet(X) & cat(X))).