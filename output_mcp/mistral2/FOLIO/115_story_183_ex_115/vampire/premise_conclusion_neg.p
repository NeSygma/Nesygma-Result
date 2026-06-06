fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(taller_peter_michael, axiom, taller_than(peter, michael)).
fof(taller_transitive, axiom, ! [X, Y, Z] : (taller_than(X, Y) & taller_than(Y, Z) => taller_than(X, Z))).
fof(taller_blocks_shooting, axiom, ! [X, Y] : (man(X) & man(Y) & taller_than(X, Y) => can_block_shooting(X, Y))).
fof(michael_taller_than_class, axiom, ! [Y] : (member_of(Y, class_members) & Y != michael => taller_than(michael, Y))).
fof(michael_blocks_non_jumpers, axiom, ! [Y] : (shooter(Y) & ~can_jump_when_shooting(Y) => can_block_shooting(michael, Y))).
fof(windy_shooter, axiom, shooter(windy)).
fof(michael_cannot_block_windy, axiom, ~can_block_shooting(michael, windy)).
fof(great_shooter_if_jumps, axiom, ! [X] : (shooter(X) & can_jump_when_shooting(X) => great_shooter(X))).

fof(class_members_include_michael, axiom, member_of(michael, class_members)).
fof(class_members_include_peter, axiom, member_of(peter, class_members)).

fof(conclusion_negation, conjecture, ~(? [Y] : (member_of(Y, class_members) & man(Y) & taller_than(Y, peter)))).