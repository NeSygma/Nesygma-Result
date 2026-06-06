fof(jane_not_likes_bark, axiom, ![X] : (bark(X) => ~likes(j, X))).
fof(dog_is_animal, axiom, ![X] : (dog(X) => animal(X))).
fof(dog_is_bark, axiom, ![X] : (dog(X) => bark(X))).
fof(jane_likes_jump, axiom, ![X] : ((animal(X) & jump(X)) => likes(j, X))).
fof(animal_has_legs_jumps, axiom, ![X] : ((animal(X) & legs(X)) => jump(X))).
fof(terricolous_has_legs, axiom, ![X] : ((animal(X) & terricolous(X)) => legs(X))).
fof(kiki_is_animal, axiom, animal(k)).
fof(kiki_conditional, axiom, ((~jump(k) & ~legs(k)) => (terricolous(k) | legs(k)))).
fof(conjecture, conjecture, (dog(k) & bark(k))).