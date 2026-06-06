fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).

% Premise 1: If a man is taller than another man, the taller one can block the other's shooting.
fof(block_rule, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block(X, Y))).

% Premise 2: Michael is taller than everyone else in his class.
fof(michael_taller_class, axiom, ! [Y] : (classmate(Y) => taller(michael, Y))).

% Premise 3: Transitivity of taller.
fof(taller_trans, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).

% Premise 4: Peter is taller than Michael.
fof(peter_taller_michael, axiom, taller(peter, michael)).

% Premise 5: Michael can block any shooting from a person as long as the person does not jump when shooting.
fof(michael_block_nojump, axiom, ! [P] : (~jump_when_shooting(P) => can_block(michael, P))).

% Premise 6: Michael cannot block Windy's shooting.
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).

% Premise 7: Every shooter who can jump when shooting is a great shooter.
fof(great_shooter_rule, axiom, ! [X] : ((shooter(X) & jump_when_shooting(X)) => great_shooter(X))).

% Negated conclusion: Peter cannot block Windy's shooting.
fof(goal, conjecture, ~can_block(peter, windy)).