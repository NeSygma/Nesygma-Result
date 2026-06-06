fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(man_windy, axiom, man(windy)).

fof(taller_transitivity, axiom, ! [X,Y,Z] : ((taller(X,Y) & taller(Y,Z)) => taller(X,Z))).

fof(taller_michael_than_class, axiom, ! [Y] : (man(Y) => taller(michael, Y))).

fof(taller_peter_than_michael, axiom, taller(peter, michael)).

fof(taller_implies_can_block, axiom, ! [X,Y] : (taller(X,Y) => can_block(X,Y))).

fof(michael_block_condition, axiom, ! [Y] : (~jumps(Y) => can_block(michael, Y))).

fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).

fof(jumps_implies_great_shooter, axiom, ! [X] : (jumps(X) => great_shooter(X))).

fof(conclusion_negation, conjecture, ~great_shooter(windy)).