fof(premise1, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block(X, Y))).
fof(premise2a, axiom, man(michael)).
fof(premise2b, axiom, ! [X] : ((in_class(X) & X != michael) => taller(michael, X))).
fof(premise3, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).
fof(premise4a, axiom, man(peter)).
fof(premise4b, axiom, taller(peter, michael)).
fof(premise5, axiom, ! [X] : (~jumps_when_shooting(X) => can_block(michael, X))).
fof(premise6, axiom, ~can_block(michael, windy)).
fof(premise7, axiom, ! [X] : (jumps_when_shooting(X) => great_shooter(X))).
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).
fof(goal, conjecture, great_shooter(windy)).