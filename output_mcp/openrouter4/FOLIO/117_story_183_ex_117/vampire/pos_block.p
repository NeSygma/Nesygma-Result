% Positive run: check if conclusion is entailed
fof(premise1, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block_shooting_of(X, Y))).
fof(premise2_man, axiom, man(michael)).
fof(premise2_class, axiom, ! [X] : ((man(X) & in_class(X, michaels_class) & X != michael) => taller(michael, X))).
fof(premise3, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).
fof(premise4, axiom, (man(peter) & taller(peter, michael))).
fof(premise5, axiom, ! [X] : ((~jumps_when_shooting(X)) => can_block_shooting_of(michael, X))).
fof(premise6, axiom, ~can_block_shooting_of(michael, windy)).
fof(premise7, axiom, ! [X] : ((shooter(X) & jumps_when_shooting(X)) => great_shooter(X))).
fof(distinct_names, axiom, (michael != peter & michael != windy & peter != windy)).
fof(conclusion, conjecture, can_block_shooting_of(peter, windy)).