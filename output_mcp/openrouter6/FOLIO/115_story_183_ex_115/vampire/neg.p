fof(distinct_constants, axiom, (michael != peter & michael != windy & peter != windy)).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(in_class_michael, axiom, in_class(michael)).
fof(premise_1, axiom, ! [X, Y] : (man(X) & man(Y) & taller_than(X, Y) => can_block_shooting(X, Y))).
fof(premise_2, axiom, ! [X] : (in_class(X) & X != michael => taller_than(michael, X))).
fof(premise_3, axiom, ! [X, Y, Z] : (taller_than(X, Y) & taller_than(Y, Z) => taller_than(X, Z))).
fof(premise_4, axiom, taller_than(peter, michael)).
fof(premise_5, axiom, ! [X] : (~jumps_when_shooting(X) => can_block_shooting(michael, X))).
fof(premise_6, axiom, ~can_block_shooting(michael, windy)).
fof(premise_7, axiom, ! [X] : (jumps_when_shooting(X) => great_shooter(X))).
fof(neg_conclusion, conjecture, ~? [X] : (man(X) & in_class(X) & taller_than(X, peter))).