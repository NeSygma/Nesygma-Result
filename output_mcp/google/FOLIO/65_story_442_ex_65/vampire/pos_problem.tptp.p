fof(p1, axiom, ! [X] : (brown_swiss(X) => cow(X))).
fof(p2, axiom, ? [X] : (pet(X) & brown_swiss(X))).
fof(p3, axiom, ! [X] : (cow(X) => domesticated(X))).
fof(p4, axiom, ! [X] : (alligator(X) => ~domesticated(X))).
fof(p5, axiom, alligator(ted)).
fof(conclusion, conjecture, (brown_swiss(ted) => ~pet(ted))).