% Negative version: Peter cannot block Windy's shooting
fof(distinct_entities, axiom, (michael != peter & michael != windy & peter != windy)).
fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(taller_michael_than_others, axiom, ! [X] : (man(X) & X != michael => taller_than(michael, X))).
fof(taller_peter_than_michael, axiom, taller_than(peter, michael)).
fof(transitivity_taller, axiom, ! [X, Y, Z] : (taller_than(X, Y) & taller_than(Y, Z) => taller_than(X, Z))).
fof(block_if_taller, axiom, ! [X, Y] : (man(X) & man(Y) & taller_than(X, Y) => can_block(X, Y))).
fof(michael_blocks_non_jumpers, axiom, ! [X] : (~jump_when_shooting(X) => can_block(michael, X))).
fof(michael_cannot_block_windy, axiom, ~can_block(michael, windy)).
fof(jumpers_are_great, axiom, ! [X] : (jump_when_shooting(X) => great_shooter(X))).
fof(goal, conjecture, ~can_block(peter, windy)).