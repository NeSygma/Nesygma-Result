% Problem: Windy is a great shooter (negated)
% Premises and conclusion (negated)

% Constants
fof(const_michael, axiom, michael = michael).
fof(const_peter, axiom, peter = peter).
fof(const_windy, axiom, windy = windy).

% Distinctness
fof(distinct_1, axiom, michael != peter).
fof(distinct_2, axiom, michael != windy).
fof(distinct_3, axiom, peter != windy).

% Person and man predicates
fof(person_michael, axiom, person(michael)).
fof(person_peter, axiom, person(peter)).
fof(person_windy, axiom, person(windy)).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).

% Class membership
fof(michael_in_class, axiom, in_class(michael)).
fof(peter_not_in_class, axiom, ~in_class(peter)).
fof(windy_not_in_class, axiom, ~in_class(windy)).

% Premise 1: If a man is taller than another man, the taller one can block the other's shooting.
fof(premise_1, axiom, ! [X, Y] : (man(X) & man(Y) & taller_than(X, Y) => can_block(X, Y))).

% Premise 2: Michael is a man who is taller than everyone else in his class.
fof(premise_2a, axiom, man(michael)).
fof(premise_2b, axiom, ! [X] : (in_class(X) & X != michael => taller_than(michael, X))).

% Premise 3: Transitivity of taller_than
fof(premise_3, axiom, ! [X, Y, Z] : (taller_than(X, Y) & taller_than(Y, Z) => taller_than(X, Z))).

% Premise 4: Peter is taller than Michael
fof(premise_4, axiom, taller_than(peter, michael)).

% Premise 5: Michael can block any shooting from a person as long as the person does not jump when shooting.
fof(premise_5, axiom, ! [X] : (person(X) & ~jumps_when_shooting(X) => can_block(michael, X))).

% Premise 6: Michael cannot block Windy's shooting.
fof(premise_6, axiom, ~can_block(michael, windy)).

% Premise 7: Every shooter who can jump when shooting is a great shooter.
fof(premise_7, axiom, ! [X] : (shooter(X) & jumps_when_shooting(X) => great_shooter(X))).

% Windy is a shooter (from premise 6, Windy's shooting implies shooter)
fof(windy_shooter, axiom, shooter(windy)).

% Negated conclusion
fof(negated_conclusion, conjecture, ~great_shooter(windy)).