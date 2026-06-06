fof(nice_not_mean, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(exists_grumpy_mean, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(animal_lover_nice, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(pet_owner_love, axiom, ! [X] : (pet_owner(X) => love_animals(X))).
fof(tom_pet_owner, axiom, pet_owner(tom)).
fof(conj, conjecture, ~grumpy(tom)).