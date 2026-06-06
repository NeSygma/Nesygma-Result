% Negative version
fof(jane_not_like_bark, axiom, ![X] : (bark(X) => ~like(jane,X))).
fof(dog_is_animal_bark, axiom, ![X] : (dog(X) => (animal(X) & bark(X)))).
fof(jane_likes_jump, axiom, ![X] : (jumps(X) => like(jane,X))).
fof(legs_imply_jump, axiom, ![X] : (animal(X) & has_legs(X) => jumps(X))).
fof(terri_imply_legs, axiom, ![X] : (animal(X) & terricolous(X) => has_legs(X))).
fof(kiki_animal, axiom, animal(kiki)).
fof(kiki_conditional, axiom, ( ~jumps(kiki) & ~has_legs(kiki) ) => ( terricolous(kiki) | has_legs(kiki) ) ).
fof(goal_neg, conjecture, ~terricolous(kiki)).