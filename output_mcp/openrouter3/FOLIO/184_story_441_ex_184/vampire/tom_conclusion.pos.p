fof(no_nice_mean, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(some_grumpy_mean, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(animal_lovers_nice, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(pet_owners_love, axiom, ! [X] : (pet_owner(X) => animal_lover(X))).
fof(tom_pet_owner, axiom, pet_owner(tom)).
fof(conclusion, conjecture, (~(grumpy(tom) & mean_to_animals(tom)) => (~grumpy(tom) & ~animal_lover(tom)))).