% Positive version
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
% Rule: taller man blocks
fof(rule_block, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).
% Michael taller than everyone else
fof(michael_taller_all, axiom, ! [Y] : (Y != michael => taller(michael,Y))).
% Transitivity of taller
fof(taller_trans, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
% Peter taller than Michael
fof(peter_taller_michael, axiom, taller(peter,michael)).
% Michael can block any non-jumping shooter
fof(michael_block_nonjump, axiom, ! [Y] : (~jump(Y) => can_block(michael,Y))).
% Michael cannot block Windy
fof(michael_not_block_windy, axiom, ~can_block(michael, windy)).
% Jumpers are great shooters (not needed for goal but include)
fof(jump_great, axiom, ! [X] : (jump(X) => great_shooter(X))).
% Goal
fof(goal, conjecture, can_block(peter, windy)).