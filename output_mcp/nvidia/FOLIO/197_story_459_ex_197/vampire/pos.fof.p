fof(axiom1, axiom, ! [X] : ((animal(X) & barks(X)) => ~likes(jane, X))).
fof(axiom2, axiom, ! [X] : (dog(X) => (animal(X) & barks(X))) ).
fof(axiom3, axiom, ! [X] : ((animal(X) & jumps(X)) => likes(jane, X))).
fof(axiom4, axiom, ! [X] : (has_legs(X) => jumps(X))).
fof(axiom5, axiom, ! [X] : (terricolous(X) => has_legs(X))).
fof(axiom6, axiom, animal(kiki)).
fof(axiom7, axiom, ( ~jumps(kiki) & ~has_legs(kiki) ) => ( terricolous(kiki) | has_legs(kiki) )).
fof(distinct_jane_kiki, axiom, jane != kiki).
fof(conjecture, conjecture, (dog(kiki) & barks(kiki))).