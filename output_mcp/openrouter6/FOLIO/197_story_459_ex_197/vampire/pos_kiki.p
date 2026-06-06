fof(premise_1, axiom, ! [X] : (animal(X) & barks(X) => ~likes_jane(X))).
fof(premise_2, axiom, ! [X] : (dog(X) => (animal(X) & barks(X)))).
fof(premise_3, axiom, ! [X] : (animal(X) & jumps(X) => likes_jane(X))).
fof(premise_4, axiom, ! [X] : (animal(X) & has_legs(X) => jumps(X))).
fof(premise_5, axiom, ! [X] : (animal(X) & terricolous(X) => has_legs(X))).
fof(premise_6, axiom, animal(kiki)).
fof(premise_7, axiom, (~jumps(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).
fof(conclusion, conjecture, dog(kiki) & barks(kiki)).