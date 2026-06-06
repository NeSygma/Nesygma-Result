fof(jane_not_likes_bark_animals, axiom, ! [X] : ((animal(X) & bark(X)) => ~likes(jane, X))).
fof(all_dogs_bark_animals, axiom, ! [X] : (dog(X) => (animal(X) & bark(X)))).
fof(jane_likes_jump_animals, axiom, ! [X] : ((animal(X) & jump(X)) => likes(jane, X))).
fof(animal_has_legs_jumps, axiom, ! [X] : ((animal(X) & legs(X)) => jump(X))).
fof(terricolous_has_legs, axiom, ! [X] : ((animal(X) & terricolous(X)) => legs(X))).
fof(kiki_is_animal, axiom, animal(kiki)).
fof(kiki_neither_jump_nor_legs_implies, axiom, (~jump(kiki) & ~legs(kiki)) => (terricolous(kiki) | legs(kiki))).
fof(conjecture, conjecture, ~terricolous(kiki)).