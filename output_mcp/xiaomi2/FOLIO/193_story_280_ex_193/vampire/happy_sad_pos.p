fof(every_event_happy_or_sad, axiom,
    ! [X] : (event(X) => (happy(X) | sad(X)))).
fof(happy_sad_exclusive, axiom,
    ! [X] : (happy(X) => ~sad(X))).
fof(at_least_one_happy, axiom,
    ? [X] : (event(X) & happy(X))).
fof(goal, conjecture,
    ! [X] : (event(X) => sad(X))).