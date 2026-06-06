% Positive run
fof(p1, axiom, ! [X] : ( (pet(X) & mammal(X)) => animal(X) ) ).
fof(p2, axiom, ! [X] : ( monkey(X) => mammal(X) ) ).
fof(p3, axiom, ! [X] : ( pet(X) => (monkey(X) | bird(X)) ) ).
fof(p4, axiom, ! [X] : ( (pet(X) & bird(X)) => can_fly(X) ) ).
fof(p5, axiom, ! [X] : ( (pet(X) & animal(X)) => can_breathe(X) ) ).
fof(p6, axiom, ! [X] : ( (pet(X) & can_fly(X)) => has_wings(X) ) ).
fof(p7, axiom, pet(rock)).
fof(p8, axiom, (can_fly(rock) | bird(rock) | ~can_breathe(rock))).
fof(goal, conjecture, has_wings(rock)).