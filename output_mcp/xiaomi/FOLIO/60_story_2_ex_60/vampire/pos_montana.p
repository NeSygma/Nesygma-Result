fof(billings_montana, axiom, in_state(billings, montana)).
fof(montana_us, axiom, in_country(montana, us)).
fof(butte_montana, axiom, in_state(butte, montana)).
fof(helena_montana, axiom, in_state(helena, montana)).
fof(missoula_montana, axiom, in_state(missoula, montana)).
fof(white_sulphur_same_state, axiom,
    ! [S] : ((in_state(white_sulphur_springs, S) & in_country(S, us)) =>
             in_state(butte, S))).
fof(butte_same_state, axiom,
    ! [S] : ((in_state(butte, S) & in_country(S, us)) =>
             in_state(white_sulphur_springs, S))).
fof(st_pierre_not_montana, axiom, ~in_state(st_pierre, montana)).
fof(butte_st_pierre_diff, axiom,
    ! [S] : ~(in_state(butte, S) & in_state(st_pierre, S))).
fof(unique_state, axiom,
    ! [C,S1,S2] : ((in_state(C, S1) & in_state(C, S2) &
                    in_country(S1, us) & in_country(S2, us)) =>
                   (S1 = S2 |
                    C = bristol | C = texarkana | C = texhoma | C = union_city))).
fof(goal, conjecture, in_state(missoula, montana)).