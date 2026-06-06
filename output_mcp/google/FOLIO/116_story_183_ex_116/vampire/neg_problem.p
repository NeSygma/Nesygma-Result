fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(michael_taller_than_others, axiom, ! [X] : ((man(X) & X != michael) => taller(michael, X))).
fof(transitivity_taller, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).
fof(peter_taller_michael, axiom, taller(peter, michael)).
fof(block_rule, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block(X, Y))).
fof(michael_block_rule, axiom, ! [X] : (~jumps(X) => can_block(michael, X))).
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).
fof(great_shooter_rule, axiom, ! [X] : (jumps(X) => great_shooter(X))).
fof(goal, conjecture, ~great_shooter(windy)).