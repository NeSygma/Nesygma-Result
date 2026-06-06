% Refined positive version: Windy is a great shooter
fof(distinct_individuals, axiom, (michael != peter & michael != windy & peter != windy)).

fof(man_michael, axiom, man(michael)).
fof(man_peter, axiom, man(peter)).
fof(man_windy, axiom, man(windy)).

fof(taller_than_peter_michael, axiom, taller_than(peter, michael)).

% Michael is taller than everyone else in his class (but Peter might not be in his class)
fof(michael_taller_than_classmates, axiom, 
    ! [X] : (man(X) & X != michael & in_class(X, michael) => taller_than(michael, X))).

fof(transitivity_taller, axiom,
    ! [X, Y, Z] : (taller_than(X, Y) & taller_than(Y, Z) => taller_than(X, Z))).

fof(blocking_by_height, axiom,
    ! [X, Y] : (man(X) & man(Y) & taller_than(X, Y) => can_block(X, Y))).

fof(michael_blocks_non_jumpers, axiom,
    ! [X] : (~can_jump_when_shooting(X) => can_block(michael, X))).

fof(michael_cannot_block_windy, axiom,
    ~can_block(michael, windy)).

fof(great_shooters_jump, axiom,
    ! [X] : (shooter(X) & can_jump_when_shooting(X) => great_shooter(X))).

fof(goal, conjecture, great_shooter(windy)).