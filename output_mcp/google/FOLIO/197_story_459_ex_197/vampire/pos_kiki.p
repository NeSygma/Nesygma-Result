fof(p1, axiom, ! [X] : (bark(X) => ~likes(jane, X))).
fof(p2, axiom, ! [X] : (dog(X) => bark(X))).
fof(p3, axiom, ! [X] : (jump(X) => likes(jane, X))).
fof(p4, axiom, ! [X] : (has_legs(X) => jump(X))).
fof(p5, axiom, ! [X] : (terricolous(X) => has_legs(X))).
fof(p6, axiom, animal(kiki)).
fof(p7, axiom, (~jump(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).
fof(goal, conjecture, (bark(kiki) & dog(kiki))).