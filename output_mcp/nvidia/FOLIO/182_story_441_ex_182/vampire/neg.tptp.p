fof(premise1, axiom, ! [X] : (nice_to_animals(X) => ~ mean_to_animals(X))).
fof(premise2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(premise3, axiom, ! [X] : (loves_animals(X) => nice_to_animals(X))).
fof(premise4, axiom, ! [X] : (pet_owner(X) => loves_animals(X))).
fof(premise5, axiom, pet_owner(tom)).
fof(conclusion, conjecture, ~grumpy(tom)).