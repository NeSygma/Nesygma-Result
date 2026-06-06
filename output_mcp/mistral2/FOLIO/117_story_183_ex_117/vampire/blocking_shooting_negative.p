fof(taller_blocks_shooting, axiom,
    ! [X, Y] : ((man(X) & man(Y) & taller(X, Y)) => can_block_shooting(X, Y))).

fof(michael_taller_than_class, axiom,
    man(michael) &
    ! [Y] : (classmate(Y) => taller(michael, Y))).

fof(transitive_taller, axiom,
    ! [X, Y, Z] : ((taller(X, Y) & taller(Y, Z)) => taller(X, Z))).

fof(peter_taller_than_michael, axiom,
    man(peter) & taller(peter, michael)).

fof(michael_blocks_if_no_jump, axiom,
    ! [Y] : (man(Y) & ~jumps_when_shooting(Y) => can_block_shooting(michael, Y))).

fof(michael_cannot_block_windy, axiom,
    ~can_block_shooting(michael, windy)).

fof(jumps_implies_great, axiom,
    ! [X] : (jumps_when_shooting(X) => great_shooter(X))).

fof(classmate_windy, axiom,
    classmate(windy)).

fof(distinct_people, axiom,
    michael != peter & michael != windy & peter != windy).

fof(conclusion_negation, conjecture,
    ~can_block_shooting(peter, windy)).