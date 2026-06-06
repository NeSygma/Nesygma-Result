fof(premise1, axiom, ! [X] : ((animal(X) & barks(X)) => ~likes_jane(X))).
fof(premise2, axiom, ! [X] : (dog(X) => (animal(X) & barks(X)))).
fof(premise3, axiom, ! [X] : ((animal(X) & jumps(X)) => likes_jane(X))).
fof(premise4, axiom, ! [X] : ((animal(X) & has_legs(X)) => jumps(X))).
fof(premise5, axiom, ! [X] : ((animal(X) & terricolous(X)) => has_legs(X))).
fof(premise6, axiom, animal(kiki)).
fof(premise7, axiom, ((~jumps(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki)))).
fof(goal, conjecture, ~barks(kiki) & ~dog(kiki)).