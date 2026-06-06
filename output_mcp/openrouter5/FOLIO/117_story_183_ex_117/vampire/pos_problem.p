% Positive version: Conjecture is "Peter can block Windy's shooting"
% Predicates:
% man(X) - X is a man
% taller(X,Y) - X is taller than Y
% can_block(X,Y) - X can block Y's shooting
% in_class(X,Y) - X is in Y's class (we'll simplify: everyone_else_in_class)
% jumps_when_shooting(X) - X jumps when shooting
% great_shooter(X) - X is a great shooter

% Premise 1: If a man is taller than another man, the taller one can block the other's shooting.
fof(premise1, axiom, ! [X,Y] : ((man(X) & man(Y) & taller(X,Y)) => can_block(X,Y))).

% Premise 2: Michael is a man who is taller than everyone else in his class.
% We interpret "everyone else in his class" as: for any person who is in Michael's class and is not Michael, Michael is taller than them.
% But we don't have explicit class membership info for all. We'll simplify: Michael is taller than everyone except himself.
% Actually, let's just assert: Michael is a man, and for any X, if X is not Michael, then taller(michael, X).
% But that's too strong. Let's be more precise: "everyone else in his class" - we only know about people in his class.
% We'll use a predicate in_same_class(X,Y) meaning X and Y are in the same class.
% Actually, let's keep it simpler. We'll just assert what we need.
fof(premise2a, axiom, man(michael)).
fof(premise2b, axiom, ! [X] : ((man(X) & X != michael) => taller(michael, X))).

% Premise 3: If person x is taller than person y, and person y is taller than person z, then x is taller than z
fof(premise3, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).

% Premise 4: Peter is a man who is taller than Michael.
fof(premise4a, axiom, man(peter)).
fof(premise4b, axiom, taller(peter, michael)).

% Premise 5: Michael can block any shooting from a person as long as the person does not jump when shooting.
fof(premise5, axiom, ! [X] : ((man(X) & ~jumps_when_shooting(X)) => can_block(michael, X))).

% Premise 6: Michael cannot block Windy's shooting.
fof(premise6, axiom, ~can_block(michael, windy)).

% Premise 7: Every shooter who can jump when shooting is a great shooter.
fof(premise7, axiom, ! [X] : ((man(X) & jumps_when_shooting(X)) => great_shooter(X))).

% Distinctness
fof(distinct, axiom, (michael != peter & michael != windy & peter != windy)).

% Conclusion: Peter can block Windy's shooting.
fof(conclusion, conjecture, can_block(peter, windy)).