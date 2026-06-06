fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(taller_peter_michael, axiom, taller(peter,michael)).
fof(taller_michael_all, axiom, ! [X] : (man(X) => taller(michael,X))).
fof(trans_taller, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
fof(block_taller, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).
fof(block_michael_nonjump, axiom, ! [Y] : (~can_jump(Y) => can_block(michael,Y))).
fof(cannot_block_michael_windy, axiom, ~can_block(michael,windy)).
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).
fof(conjecture, conjecture, can_block(peter,windy)).