% Negative problem: prove ~great_shooter(windy)
fof(distinct_names, axiom, (michael != peter & michael != windy & peter != windy)).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(taller_trans, axiom, ! [X,Y,Z] : (taller(X,Y) & taller(Y,Z) => taller(X,Z))).
fof(taller_block_rule, axiom, ! [X,Y] : (man(X) & man(Y) & taller(X,Y) => can_block(X,Y))).
fof(michael_taller_all, axiom, ! [Y] : (Y != michael => taller(michael,Y))).
fof(peter_taller_michael, axiom, taller(peter,michael)).
fof(michael_block_nonjump, axiom, ! [X] : (~jumps(X) => can_block(michael,X))).
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).
fof(jump_great, axiom, ! [X] : (jumps(X) => great_shooter(X))).
fof(goal, conjecture, ~great_shooter(windy)).