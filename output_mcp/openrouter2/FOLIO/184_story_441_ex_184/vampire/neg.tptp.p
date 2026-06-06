fof(nice_implies_not_mean, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(exist_grumpy_mean, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(animal_lover_implies_nice, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(pet_owner_implies_love, axiom, ! [X] : (pet_owner(X) => love_animals(X))).
fof(tom_pet_owner, axiom, pet_owner(tom)).
fof(conjecture, conjecture, ~((~(grumpy(tom) & mean_to_animals(tom))) => (~grumpy(tom) & ~animal_lover(tom)))).