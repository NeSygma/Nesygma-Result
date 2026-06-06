% Negative file: negated conclusion as conjecture
fof(distinct_names, axiom, (michael != peter & michael != windy & peter != windy)).

% Taller is irreflexive and antisymmetric
fof(taller_irrefl, axiom, ! [X] : ~taller(X, X)).
fof(taller_antisym, axiom, ! [X, Y] : (taller(X, Y) => ~taller(Y, X))).

% Premise 1: If a man is taller than another man, the taller one can block the other's shooting.
fof(premise_1, axiom, ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block(X, Y))).

% Premise 2: Michael is a man who is taller than everyone else in his class.
fof(premise_2a, axiom, man(michael)).
fof(premise_2b, axiom, ! [X] : ((in_michael_class(X) & X != michael) => taller(michael, X))).
% Michael is in his own class
fof(premise_2c, axiom, in_michael_class(michael)).

% Premise 3: Transitivity of taller
fof(premise_3, axiom, ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).

% Premise 4: Peter is a man who is taller than Michael.
fof(premise_4a, axiom, man(peter)).
fof(premise_4b, axiom, taller(peter, michael)).

% Premise 5: Michael can block any shooting from a person who does not jump when shooting.
fof(premise_5, axiom, ! [P] : ((person(P) & ~jumps(P)) => can_block(michael, P))).

% Premise 6: Michael cannot block Windy's shooting.
fof(premise_6, axiom, ~can_block(michael, windy)).

% Premise 7: Every shooter who can jump when shooting is a great shooter.
fof(premise_7, axiom, ! [X] : ((shooter(X) & jumps(X)) => great_shooter(X))).

% Definition of shorter
fof(shorter_def, axiom, ! [X, Y] : (shorter(X, Y) <=> taller(Y, X))).

% Negated conclusion: It is NOT the case that Peter is shorter than a man in Michael's class.
fof(neg_conclusion, conjecture, ~? [X] : (man(X) & in_michael_class(X) & shorter(peter, X))).