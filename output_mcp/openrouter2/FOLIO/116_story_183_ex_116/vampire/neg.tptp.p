fof(michael_is_man, axiom, man(michael)).
fof(peter_is_man, axiom, man(peter)).
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).
fof(michael_taller_all, axiom, ![Y] : ((man(Y) & Y != michael) => taller(michael,Y))).
fof(peter_taller_michael, axiom, taller(peter,michael)).
fof(taller_block_rule, axiom, ![X,Y] : ((man(X) & man(Y) & taller(X,Y)) => block(X,Y))).
fof(taller_trans, axiom, ![X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
fof(michael_block_rule, axiom, ![Y] : (~jump(Y) => block(michael,Y))).
fof(michael_cannot_block_windy, axiom, ~block(michael,windy)).
fof(shooter_jump_great, axiom, ![X] : ((shooter(X) & jump(X)) => great_shooter(X))).
fof(conjecture, conjecture, ~great_shooter(windy)).