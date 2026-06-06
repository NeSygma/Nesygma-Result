% Negative claim: Butte and St Pierre are NOT in the same state.
fof(distinct_cities, axiom,
    (billings != butte & billings != helena & billings != missoula &
     billings != white_sulphur_springs & billings != st_pierre &
     billings != bristol & billings != texarkana & billings != texhoma &
     billings != union_city & billings != montana &
     butte != helena & butte != missoula & butte != white_sulphur_springs &
     butte != st_pierre & butte != bristol & butte != texarkana &
     butte != texhoma & butte != union_city & butte != montana &
     helena != missoula & helena != white_sulphur_springs &
     helena != st_pierre & helena != bristol & helena != texarkana &
     helena != texhoma & helena != union_city & helena != montana &
     missoula != white_sulphur_springs & missoula != st_pierre &
     missoula != bristol & missoula != texarkana & missoula != texhoma &
     missoula != union_city & missoula != montana &
     white_sulphur_springs != st_pierre & white_sulphur_springs != bristol &
     white_sulphur_springs != texarkana & white_sulphur_springs != texhoma &
     white_sulphur_springs != union_city & white_sulphur_springs != montana &
     st_pierre != bristol & st_pierre != texarkana & st_pierre != texhoma &
     st_pierre != union_city & st_pierre != montana &
     bristol != texarkana & bristol != texhoma & bristol != union_city &
     bristol != montana & texarkana != texhoma & texarkana != union_city &
     texarkana != montana & texhoma != union_city & texhoma != montana &
     union_city != montana)).

fof(premise1, axiom, in_state(billings, montana)).

fof(premise2a, axiom, in_state(butte, montana)).
fof(premise2b, axiom, in_state(helena, montana)).
fof(premise2c, axiom, in_state(missoula, montana)).

fof(premise3, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).

fof(premise4, axiom, ~in_state(st_pierre, montana)).

fof(premise5, axiom, ! [X] : (located_in(X, butte) => ~located_in(X, st_pierre))).

fof(premise6, axiom,
    ! [C, S1, S2] :
        ((C != bristol & C != texarkana & C != texhoma & C != union_city &
          in_state(C, S1) & in_state(C, S2))
         => S1 = S2)).

% Negated conclusion: Butte and St Pierre are NOT in the same state.
fof(goal_neg, conjecture, ~? [S] : (in_state(butte, S) & in_state(st_pierre, S))).