% Negative version (negated goal)
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(rule_block, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).
fof(michael_taller_all, axiom, ! [Y] : (Y != michael => taller(michael,Y))).
fof(taller_trans, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
fof(peter_taller_michael, axiom, taller(peter,michael)).
fof(michael_block_nonjump, axiom, ! [Y] : (~jump(Y) => can_block(michael,Y))).
fof(michael_not_block_windy, axiom, ~can_block(michael, windy)).
fof(jump_great, axiom, ! [X] : (jump(X) => great_shooter(X))).
fof(goal_neg, conjecture, ~can_block(peter, windy)).