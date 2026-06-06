% Negative conjecture: no man in Michael's class is taller than Peter
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(man_windy, axiom, man(windy)).
fof(in_class_michael, axiom, in_class(michael)).
fof(distinct1, axiom, michael != peter).
fof(distinct2, axiom, michael != windy).
fof(distinct3, axiom, peter != windy).
fof(taller_trans, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
fof(michael_taller_class, axiom, ! [Z] : ((in_class(Z) & Z != michael) => taller(michael, Z))).
fof(peter_taller_michael, axiom, taller(peter, michael)).
fof(taller_block, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => block(X,Y))).
fof(michael_block_if_not_jump, axiom, ! [Y] : ((man(Y) & ~jump(Y)) => block(michael, Y))).
fof(michael_cannot_block_windy, axiom, ~block(michael, windy)).
fof(jump_great, axiom, ! [Y] : (jump(Y) => great_shooter(Y))).
% Negative conjecture
fof(goal_neg, conjecture, ! [X] : ((man(X) & in_class(X)) => ~taller(X, peter))).