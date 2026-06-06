fof(premise1, axiom,
    ! [X, Y] : ((man(X) & man(Y) & taller_than(X, Y)) => can_block(X, Y))).

fof(premise2, axiom,
    man(michael) &
    ! [Y] : (Y != michael => taller_than(michael, Y))).

fof(premise3, axiom,
    ! [X, Y, Z] : ((taller_than(X, Y) & taller_than(Y, Z)) => taller_than(X, Z))).

fof(premise4, axiom,
    man(peter) & taller_than(peter, michael)).

fof(premise5, axiom,
    ! [Y] : (man(Y) & ~jumps_when_shooting(Y) => can_block(michael, Y))).

fof(premise6, axiom,
    ~can_block(michael, windy)).

fof(premise7, axiom,
    ! [X] : (jumps_when_shooting(X) => great_shooter(X))).

fof(conclusion, conjecture,
    great_shooter(windy)).