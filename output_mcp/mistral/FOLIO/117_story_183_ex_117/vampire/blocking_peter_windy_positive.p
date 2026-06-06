fof(michael_is_man, axiom, man(michael)).
fof(peter_is_man, axiom, man(peter)).
fof(windy_is_shooter, axiom, shooter(windy)).
fof(taller_transitivity, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
fof(taller_peter_michael, axiom, taller(peter, michael)).
fof(michael_taller_than_class, axiom, ! [Y] : ((Y != michael & in_class_michaels_class(Y)) => taller(michael, Y))).
fof(michael_in_class, axiom, in_class_michaels_class(michael)).
fof(blocking_rule, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).
fof(michael_blocking_rule, axiom, ! [Y] : ((shooter(Y) & ~jumps(Y)) => can_block(michael, Y))).
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).
fof(great_shooter_rule, axiom, ! [X] : ((shooter(X) & jumps(X)) => great_shooter(X))).
fof(goal, conjecture, can_block(peter, windy)).