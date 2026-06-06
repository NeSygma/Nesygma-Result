% Positive version: original conclusion as conjecture
% Conclusion: KiKi does not bark and he is not a dog.
% i.e., ~bark(kiki) & ~dog(kiki)

fof(premise_1, axiom, ! [X] : (animal(X) & bark(X) => ~likes(jane, X))).
fof(premise_2, axiom, ! [X] : (dog(X) => (animal(X) & bark(X)))).
fof(premise_3, axiom, ! [X] : (animal(X) & jump(X) => likes(jane, X))).
fof(premise_4, axiom, ! [X] : (animal(X) & has_legs(X) => jump(X))).
fof(premise_5, axiom, ! [X] : (animal(X) & terricolous(X) => has_legs(X))).
fof(premise_6, axiom, animal(kiki)).
fof(premise_7, axiom, ! [X] : ((animal(X) & ~jump(X) & ~has_legs(X)) => (terricolous(X) | has_legs(X)))).

fof(goal, conjecture, (~bark(kiki) & ~dog(kiki))).