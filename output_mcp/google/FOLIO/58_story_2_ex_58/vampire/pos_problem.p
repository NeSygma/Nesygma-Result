fof(city_in_state, axiom, ! [C, S1, S2] : ((in_state(C, S1) & in_state(C, S2) & ~exception(C)) => S1 = S2)).
fof(exception_list, axiom, ! [C] : (exception(C) <=> (C = bristol | C = texarkana | C = texhoma | C = union_city))).
fof(billings_in_mt, axiom, in_state(billings, montana)).
fof(mt_cities, axiom, (in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana))).
fof(wss_butte_same, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(sp_not_in_mt, axiom, ~in_state(st_pierre, montana)).
fof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)).
fof(goal, conjecture, ? [S] : (in_state(butte, S) & in_state(st_pierre, S))).