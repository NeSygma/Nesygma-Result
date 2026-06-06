fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).

% Premise 1: If a man is taller than another man, the taller one can block the other's shooting
fof(block_rule, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).

% Premise 2: Michael is taller than everyone in his class
fof(michael_taller_class, axiom, ! [X] : (in_class(X, michael) => taller(michael, X))).

% Premise 3: Transitivity of taller
fof(taller_trans, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).

% Premise 4: Peter is taller than Michael
fof(peter_taller_michael, axiom, taller(peter, michael)).

% Premise 5: Michael can block any shooting from a person who does not jump when shooting
fof(michael_block_nojump, axiom, ! [X] : (~jumps_when_shooting(X) => can_block(michael, X))).

% Premise 6: Michael cannot block Windy's shooting
fof(michael_not_block_windy, axiom, ~can_block(michael, windy)).

% Premise 7: Every shooter who can jump when shooting is a great shooter
fof(jump_great, axiom, ! [X] : (jumps_when_shooting(X) => great_shooter(X))).

% Negated conclusion: Peter is NOT shorter than any man in Michael's class
% i.e., for all X, if man(X) and in_class(X, michael), then NOT taller(X, peter)
fof(goal, conjecture, ~? [X] : (man(X) & in_class(X, michael) & taller(X, peter))).