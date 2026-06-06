fof(premise1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(premise2, axiom, ? [X] : (grumpy_person(X) & mean_to_animals(X))).
fof(premise3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(premise4, axiom, ! [X] : (pet_owner(X) => love_animals(X))).
fof(premise5, axiom, pet_owner(tom)).
fof(goal, conjecture, ~grumpy_person(tom)).