% Positive file: Peter can block Windy's shooting
fof(distinct_constants, axiom, (michael != peter & michael != windy & peter != windy)).
fof(person_type, axiom, person(michael) & person(peter) & person(windy)).
fof(man_type, axiom, man(michael) & man(peter)).
fof(premise_1, axiom, ! [X, Y] : (man(X) & man(Y) & taller_than(X, Y) => can_block(X, Y))).
fof(premise_2, axiom, man(michael) & ! [X] : (X != michael & in_class(X) => taller_than(michael, X))).
fof(premise_3, axiom, ! [X, Y, Z] : (taller_than(X, Y) & taller_than(Y, Z) => taller_than(X, Z))).
fof(premise_4, axiom, man(peter) & taller_than(peter, michael)).
fof(premise_5, axiom, ! [X] : (person(X) & ~can_jump_when_shooting(X) => can_block(michael, X))).
fof(premise_6, axiom, ~can_block(michael, windy)).
fof(premise_7, axiom, ! [X] : (shooter(X) & can_jump_when_shooting(X) => great_shooter(X))).
fof(windy_jumps, axiom, can_jump_when_shooting(windy)). % Derived from premises 5 & 6
fof(conclusion, conjecture, can_block(peter, windy)).