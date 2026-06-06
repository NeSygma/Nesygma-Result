% Positive version
fof(jane_no_like_bark, axiom, ! [X] : ((animal(X) & bark(X)) => ~likes(jane, X))).
fof(all_dogs_bark, axiom, ! [X] : (dog(X) => (animal(X) & bark(X)))).
fof(jane_likes_jump, axiom, ! [X] : ((animal(X) & jumps(X)) => likes(jane, X))).
fof(legs_implies_jump, axiom, ! [X] : ((animal(X) & has_legs(X)) => jumps(X))).
fof(terri_implies_legs, axiom, ! [X] : ((animal(X) & terricolous(X)) => has_legs(X))).
fof(kiki_animal, axiom, animal(kiki)).
fof(kiki_conditional, axiom, ((~jumps(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki)))).
fof(goal, conjecture, dog(kiki) & bark(kiki)).