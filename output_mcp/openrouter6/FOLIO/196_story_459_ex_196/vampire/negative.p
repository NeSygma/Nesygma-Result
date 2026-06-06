fof(premise1, axiom, ! [X] : (animal(X) & bark(X) => ~like_jane(X))).
fof(premise2, axiom, ! [X] : (dog(X) => animal(X) & bark(X))).
fof(premise3, axiom, ! [X] : (animal(X) & jump(X) => like_jane(X))).
fof(premise4, axiom, ! [X] : (animal(X) & has_legs(X) => jump(X))).
fof(premise5, axiom, ! [X] : (animal(X) & terricolous(X) => has_legs(X))).
fof(premise6, axiom, animal(kiki)).
fof(premise7, axiom, (~jump(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).
fof(goal, conjecture, ~terricolous(kiki)).