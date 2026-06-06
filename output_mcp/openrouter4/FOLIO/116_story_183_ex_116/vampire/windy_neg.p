% Negative version: Conjecture is the negation of "Windy is a great shooter"
fof(premise1, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block(X, Y))).
fof(premise2a, axiom, man(michael)).
fof(premise2b, axiom, ! [X] : ((in_michaels_class(X) & X != michael) => taller(michael, X))).
fof(premise3, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).
fof(premise4a, axiom, man(peter)).
fof(premise4b, axiom, taller(peter, michael)).
fof(premise5, axiom, ! [X] : ((person(X) & ~jumps_when_shooting(X)) => can_block(michael, X))).
fof(premise6, axiom, ~can_block(michael, windy)).
fof(premise7, axiom, ! [X] : ((shooter(X) & jumps_when_shooting(X)) => great_shooter(X))).

% Implicit premises from context: Windy's shooting is discussed, so Windy is a person and a shooter
fof(windy_person, axiom, person(windy)).
fof(windy_shooter, axiom, shooter(windy)).

% Distinctness of named individuals
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).

fof(conclusion_neg, conjecture, ~great_shooter(windy)).