fof(billings_in_montana, axiom, in_city(billings, montana)).
fof(montana_cities, axiom, in_city(butte, montana) & in_city(helena, montana) & in_city(missoula, montana)).
fof(white_sulphur_same_state_as_butte, axiom, same_state(white_sulphur_springs, butte)).
fof(st_pierre_not_in_montana, axiom, ~in_city(st_pierre, montana)).
fof(butte_not_in_st_pierre, axiom, ~in_city(butte, st_pierre)).
fof(city_distinctness, axiom, billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre).
fof(same_state_symmetry, axiom, ! [C1, C2] : (same_state(C1, C2) => same_state(C2, C1))).
fof(same_state_transitivity, axiom, ! [C1, C2, C3] : ((same_state(C1, C2) & same_state(C2, C3)) => same_state(C1, C3))).
fof(same_state_implies_same_location, axiom, ! [C1, C2, S] : ((same_state(C1, C2) & in_city(C1, S)) => in_city(C2, S))).
fof(conclusion, conjecture, in_city(missoula, montana)).