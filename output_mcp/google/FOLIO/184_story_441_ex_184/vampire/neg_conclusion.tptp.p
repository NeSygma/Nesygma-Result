fof(p1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(p2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(p3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(p4, axiom, ! [X] : (pet_owner(X) => animal_lover(X))).
fof(p5, axiom, pet_owner(tom)).
fof(conclusion, conjecture, ~ (~(grumpy(tom) & mean_to_animals(tom)) => (~grumpy(tom) & ~animal_lover(tom)))).