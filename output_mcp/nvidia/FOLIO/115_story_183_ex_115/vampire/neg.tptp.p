fof(axiom_block, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).
fof(axiom_michael_man, axiom, man(michael)).
fof(axiom_michael_taller, axiom, ! [X] : ((class(michael, X) & X != michael) => taller(michael, X))).
fof(axiom_trans, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
fof(axiom_peter_man, axiom, man(peter)).
fof(axiom_peter_taller, axiom, taller(peter, michael)).
fof(axiom_block_nojump, axiom, ! [X] : ((man(X) & ~jump(X)) => can_block(michael, X))).
fof(axiom_cannot_block_windy, axiom, ~can_block(michael, windy)).
fof(axiom_shooter_jump, axiom, ! [X] : ((shooter(X) & jump(X)) => great_shooter(X))).
fof(goal, conjecture, ~ ? [Y] : (man(Y) & class(michael, Y) & taller(Y, peter))).