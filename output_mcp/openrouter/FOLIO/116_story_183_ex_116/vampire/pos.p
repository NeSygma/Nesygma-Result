% Positive problem: prove great_shooter(windy)
fof(distinct_names, axiom, (michael != peter & michael != windy & peter != windy)).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
% taller transitivity
fof(taller_trans, axiom, ! [X,Y,Z] : (taller(X,Y) & taller(Y,Z) => taller(X,Z))).
% rule: taller man can block
fof(taller_block_rule, axiom, ! [X,Y] : (man(X) & man(Y) & taller(X,Y) => can_block(X,Y))).
% Michael taller than everyone else
fof(michael_taller_all, axiom, ! [Y] : (Y != michael => taller(michael,Y))).
% Peter taller than Michael
fof(peter_taller_michael, axiom, taller(peter,michael)).
% Michael can block any non-jumping shooter
fof(michael_block_nonjump, axiom, ! [X] : (~jumps(X) => can_block(michael,X))).
% Michael cannot block Windy
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).
% Jumpers are great shooters
fof(jump_great, axiom, ! [X] : (jumps(X) => great_shooter(X))).
% Conjecture
fof(goal, conjecture, great_shooter(windy)).