fof(premise_1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(premise_2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(premise_3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(premise_4, axiom, ! [X] : (pet_owner(X) => animal_lover(X))).
fof(premise_5, axiom, pet_owner(tom)).
fof(goal_negation, conjecture, ~grumpy(tom)).