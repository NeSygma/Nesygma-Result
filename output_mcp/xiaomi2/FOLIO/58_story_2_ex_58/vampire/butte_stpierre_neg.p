fof(p1, axiom, city_in_state(billings, montana)).
fof(p2a, axiom, city_in_state(butte, montana)).
fof(p2b, axiom, city_in_state(helena, montana)).
fof(p2c, axiom, city_in_state(missoula, montana)).
fof(p3, axiom, city_in_state(white_sulphur_springs, montana)).
fof(p4, axiom, ~city_in_state(st_pierre, montana)).
fof(p5, axiom, ! [S] : (city_in_state(butte, S) => ~city_in_state(st_pierre, S))).
fof(p6, axiom, ! [C, S1, S2] :
    ((city_in_state(C, S1) & city_in_state(C, S2) &
      C != bristol & C != texarkana & C != texhoma & C != union_city)
     => S1 = S2)).
fof(distinct_cities, axiom, (
    billings != butte & billings != helena & billings != missoula &
    billings != white_sulphur_springs & billings != st_pierre &
    billings != bristol & billings != texarkana & billings != texhoma & billings != union_city &
    butte != helena & butte != missoula & butte != white_sulphur_springs &
    butte != st_pierre & butte != bristol & butte != texarkana & butte != texhoma & butte != union_city &
    helena != missoula & helena != white_sulphur_springs & helena != st_pierre &
    helena != bristol & helena != texarkana & helena != texhoma & helena != union_city &
    missoula != white_sulphur_springs & missoula != st_pierre &
    missoula != bristol & missoula != texarkana & missoula != texhoma & missoula != union_city &
    white_sulphur_springs != st_pierre & white_sulphur_springs != bristol &
    white_sulphur_springs != texarkana & white_sulphur_springs != texhoma & white_sulphur_springs != union_city &
    st_pierre != bristol & st_pierre != texarkana & st_pierre != texhoma & st_pierre != union_city &
    bristol != texarkana & bristol != texhoma & bristol != union_city &
    texarkana != texhoma & texarkana != union_city &
    texhoma != union_city
)).
fof(goal, conjecture, ~? [S] : (city_in_state(butte, S) & city_in_state(st_pierre, S))).