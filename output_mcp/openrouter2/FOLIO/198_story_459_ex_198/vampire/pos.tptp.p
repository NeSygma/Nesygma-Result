fof(jane_dislikes_bark_animals, axiom, ![X] : ((animal(X) & bark(X)) => ~likes(jane, X))).
fof(dog_implies_animal_and_bark, axiom, ![X] : (dog(X) => (animal(X) & bark(X)))).
fof(jane_likes_jump_animals, axiom, ![X] : ((animal(X) & jump(X)) => likes(jane, X))).
fof(legs_implies_jump, axiom, ![X] : ((animal(X) & legs(X)) => jump(X))).
fof(terricolous_implies_legs, axiom, ![X] : ((animal(X) & terricolous(X)) => legs(X))).
fof(kiki_is_animal, axiom, animal(kiki)).
fof(kiki_rule, axiom, ((~jump(kiki) & ~legs(kiki)) => (terricolous(kiki) | legs(kiki)))).
fof(distinct, axiom, jane != kiki).
fof(goal, conjecture, (~bark(kiki) & ~dog(kiki))).