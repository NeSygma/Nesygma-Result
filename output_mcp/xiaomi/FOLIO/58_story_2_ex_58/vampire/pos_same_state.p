fof(billings_montana, axiom, in_state(billings, montana)).
fof(butte_montana, axiom, in_state(butte, montana)).
fof(helena_montana, axiom, in_state(helena, montana)).
fof(missoula_montana, axiom, in_state(missoula, montana)).
fof(white_sulphur_same_state_as_butte, axiom,
    ! [S] : (in_state(butte, S) => in_state(white_sulphur_springs, S))).
fof(st_pierre_not_montana, axiom, ~in_state(st_pierre, montana)).
fof(butte_not_st_pierre, axiom, butte != st_pierre).
fof(one_state_except_exceptions, axiom,
    ! [C, S1, S2] :
        ((in_state(C, S1) & in_state(C, S2) &
          C != bristol & C != texarkana & C != texhoma & C != union_city)
        => S1 = S2)).
fof(goal, conjecture,
    ? [S] : (in_state(butte, S) & in_state(st_pierre, S))).