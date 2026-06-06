% Positive conjecture: there exists a man in Michael's class taller than Peter
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(man_windy, axiom, man(windy)).
fof(in_class_michael, axiom, in_class(michael)).
% distinctness
fof(distinct1, axiom, michael != peter).
fof(distinct2, axiom, michael != windy).
fof(distinct3, axiom, peter != windy).
% taller transitivity
fof(taller_trans, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).
% Michael taller than everyone else in his class
fof(michael_taller_class, axiom, ! [Z] : ((in_class(Z) & Z != michael) => taller(michael, Z))).
% Peter taller than Michael
fof(peter_taller_michael, axiom, taller(peter, michael)).
% If a man is taller than another man, the taller can block the other's shooting (not needed for conclusion)
fof(taller_block, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => block(X,Y))).
% Michael can block any shooting from a person as long as the person does not jump when shooting
fof(michael_block_if_not_jump, axiom, ! [Y] : ((man(Y) & ~jump(Y)) => block(michael, Y))).
% Michael cannot block Windy's shooting
fof(michael_cannot_block_windy, axiom, ~block(michael, windy)).
% Every shooter who can jump when shooting is a great shooter
fof(jump_great, axiom, ! [Y] : (jump(Y) => great_shooter(Y))).
% Positive conjecture
fof(goal_pos, conjecture, ? [X] : (man(X) & in_class(X) & taller(X, peter))).