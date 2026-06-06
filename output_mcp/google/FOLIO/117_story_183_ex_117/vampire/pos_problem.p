fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(taller_transitive, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).
fof(michael_taller_than_class, axiom, ! [X] : ((in_class(X) & X != michael) => taller(michael, X))).
fof(peter_taller_michael, axiom, taller(peter, michael)).
fof(block_rule, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block(X, Y))).
fof(michael_block_rule, axiom, ! [P] : (~jumps(P) => can_block(michael, P))).
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).
fof(jumps_great_shooter, axiom, ! [P] : (jumps(P) => great_shooter(P))).
fof(windy_in_class, axiom, in_class(windy)).
fof(windy_is_man, axiom, man(windy)).
fof(goal, conjecture, can_block(peter, windy)).