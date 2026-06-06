% Negative file: negated claim as conjecture
% Predicates:
% man(X) - X is a man
% taller(X,Y) - X is taller than Y
% can_block(X,Y) - X can block Y's shooting
% jumps_when_shooting(X) - X jumps when shooting
% great_shooter(X) - X is a great shooter

% Distinct constants
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).

% If a man is taller than another man, the taller one can block the other's shooting.
fof(rule1, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).

% Michael is a man who is taller than everyone else in his class.
fof(fact1, axiom, man(michael)).
fof(fact2, axiom, ! [X] : ((man(X) & X != michael) => taller(michael, X))).

% If person x is taller than person y, and person y is taller than person z, then x is taller than z
fof(rule2, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).

% Peter is a man who is taller than Michael.
fof(fact3, axiom, man(peter)).
fof(fact4, axiom, taller(peter, michael)).

% Michael can block any shooting from a person as long as the person does not jump when shooting.
fof(rule3, axiom, ! [X] : ((~jumps_when_shooting(X)) => can_block(michael, X))).

% Michael cannot block Windy's shooting.
fof(fact5, axiom, ~can_block(michael, windy)).

% Every shooter who can jump when shooting is a great shooter.
fof(rule4, axiom, ! [X] : (jumps_when_shooting(X) => great_shooter(X))).

% Negated conclusion: Windy is NOT a great shooter.
fof(goal, conjecture, ~great_shooter(windy)).