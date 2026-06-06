fof(p1, axiom, ! [X] : ((animal(X) & barks(X)) => ~likes(jane, X))).
fof(p2, axiom, ! [X] : (dog(X) => (animal(X) & barks(X)))).
fof(p3, axiom, ! [X] : ((animal(X) & jumps(X)) => likes(jane, X))).
fof(p4, axiom, ! [X] : ((animal(X) & has_legs(X)) => jumps(X))).
fof(p5, axiom, ! [X] : ((animal(X) & terricolous(X)) => has_legs(X))).
fof(p6, axiom, animal(kiki)).
fof(p7, axiom, ((~jumps(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki)))).
fof(goal, conjecture, dog(kiki) & barks(kiki)).