fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).

% Premise 1: If a man is taller than another man, the taller one can block the other's shooting
fof(taller_blocks, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block(X, Y))).

% Premise 2: Michael is taller than everyone else in his class
fof(michael_taller, axiom, ! [Y] : ((man(Y) & Y != michael) => taller(michael, Y))).

% Premise 3: Transitivity of taller
fof(taller_trans, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).

% Premise 4: Peter is taller than Michael
fof(peter_taller_michael, axiom, taller(peter, michael)).

% Premise 5: Michael can block any shooting from a person as long as the person does not jump when shooting
fof(michael_block_no_jump, axiom, ! [X] : ((shoots(X) & ~jumps_when_shooting(X)) => can_block(michael, X))).

% Premise 6: Michael cannot block Windy's shooting
fof(cannot_block_windy, axiom, ~can_block(michael, windy)).

% Premise 7: Every shooter who can jump when shooting is a great shooter
fof(jump_great, axiom, ! [X] : ((shoots(X) & jumps_when_shooting(X)) => great_shooter(X))).

% Windy is a shooter (implicit from "Michael cannot block Windy's shooting")
fof(windy_shoots, axiom, shoots(windy)).

% Conclusion: Windy is a great shooter
fof(goal, conjecture, great_shooter(windy)).