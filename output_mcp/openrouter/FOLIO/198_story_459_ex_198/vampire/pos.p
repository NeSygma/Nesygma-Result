% Positive check: KiKi does not bark and is not a dog
fof(distinct_names, axiom, (jane != kiki)).
fof(jane_not_like_bark, axiom, ![X] : ((animal(X) & bark(X)) => ~likes(jane,X))).
fof(all_dogs_bark, axiom, ![X] : (dog(X) => (animal(X) & bark(X)))).
fof(jane_likes_jump, axiom, ![X] : ((animal(X) & jump(X)) => likes(jane,X))).
fof(legs_implies_jump, axiom, ![X] : ((animal(X) & has_legs(X)) => jump(X))).
fof(terri_implies_legs, axiom, ![X] : ((animal(X) & terricolous(X)) => has_legs(X))).
fof(kiki_animal, axiom, animal(kiki)).
fof(kiki_conditional, axiom, ((~jump(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki)))).
fof(goal, conjecture, (~bark(kiki) & ~dog(kiki))).