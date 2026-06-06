fof(axiom1, axiom, ![X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(axiom2, axiom, ?[X] : (grumpy(X) & mean_to_animals(X))).
fof(axiom3, axiom, ![X] : (animal_lover(X) => nice_to_animals(X))).
fof(axiom4, axiom, ![X] : (pet_owner(X) => loves_animals(X))).
fof(fact1, axiom, pet_owner(tom)).
fof(conjecture, conjecture, ~ (grumpy(tom) & mean_to_animals(tom))).