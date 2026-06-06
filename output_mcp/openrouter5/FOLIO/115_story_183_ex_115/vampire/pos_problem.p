% Positive version: original conclusion as conjecture
% Conclusion: Peter is shorter than a man in Michael's class.
% i.e., There exists a man M in Michael's class such that Peter is shorter than M.
% "shorter than" = converse of "taller than": shorter(X,Y) <=> taller(Y,X)

fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).

% If a man is taller than another man, the taller one can block the other's shooting.
fof(rule1, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block_shooting_of(X,Y))).

% Michael is a man who is taller than everyone else in his class.
fof(michael_man, axiom, man(michael)).
fof(michael_taller_class, axiom, ! [X] : ((man(X) & in_class(X, michaels_class) & X != michael) => taller(michael, X))).

% If person x is taller than person y, and person y is taller than person z, then x is taller than z
fof(transitivity, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).

% Peter is a man who is taller than Michael.
fof(peter_man, axiom, man(peter)).
fof(peter_taller_michael, axiom, taller(peter, michael)).

% Michael can block any shooting from a person as long as the person does not jump when shooting.
fof(rule2, axiom, ! [X] : ((person(X) & ~jumps_when_shooting(X)) => can_block_shooting_of(michael, X))).

% Michael cannot block Windy's shooting.
fof(rule3, axiom, ~can_block_shooting_of(michael, windy)).

% Every shooter who can jump when shooting is a great shooter.
fof(rule4, axiom, ! [X] : ((shooter(X) & jumps_when_shooting(X)) => great_shooter(X))).

% Additional needed: every man is a person
fof(man_is_person, axiom, ! [X] : (man(X) => person(X))).

% Windy is a person (shooter implied)
fof(windy_person, axiom, person(windy)).
fof(windy_shooter, axiom, shooter(windy)).

% Conclusion: Peter is shorter than a man in Michael's class.
% shorter(X,Y) <=> taller(Y,X)
fof(goal, conjecture, ? [M] : (man(M) & in_class(M, michaels_class) & taller(M, peter))).