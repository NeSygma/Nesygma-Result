fof(premise1, axiom, ! [X] : (nice(X) => ~mean(X))).
fof(premise2, axiom, ? [X] : (grumpy(X) & mean(X))).
fof(premise3, axiom, ! [X] : (animal_lover(X) => nice(X))).
fof(premise4, axiom, ! [X] : (pet_owner(X) => loves_animals(X))).
fof(premise5, axiom, pet_owner(tom)).
fof(grumpy_mean_person, axiom, grumpy(alice) & mean(alice)).
fof(distinct, axiom, tom != alice).
fof(conclusion, conjecture, ( ~(grumpy(tom) & mean(tom)) ) => ( ~grumpy(tom) & ~animal_lover(tom) )).