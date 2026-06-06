fof(premise1, axiom, ! [X] : (cat(X) => mammal(X))).
fof(premise2, axiom, ? [X] : (pet(X) & ~mammal(X))).
fof(neg_conclusion, conjecture, ? [X] : (pet(X) & cat(X))).