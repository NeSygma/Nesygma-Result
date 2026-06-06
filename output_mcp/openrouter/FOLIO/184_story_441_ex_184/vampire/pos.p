% Positive run
fof(premise1, axiom, ! [X] : (nice(X) => ~mean(X))).
fof(premise2, axiom, ? [X] : (grumpy(X) & mean(X))).
fof(premise3, axiom, ! [X] : (lover(X) => nice(X))).
fof(premise4, axiom, ! [X] : (pet_owner(X) => love_animals(X))).
fof(premise5, axiom, pet_owner(tom)).
fof(conclusion, conjecture, ( ~ (grumpy(tom) & mean(tom)) ) => ( ~grumpy(tom) & ~lover(tom) )).