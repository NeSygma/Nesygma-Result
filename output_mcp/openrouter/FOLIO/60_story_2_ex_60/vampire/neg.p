% Negative version
fof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)).
fof(in_state_fact1, axiom, in_state(billings, montana)).
fof(in_state_fact2, axiom, in_state(butte, montana)).
fof(in_state_fact3, axiom, in_state(helena, montana)).
fof(in_state_fact4, axiom, in_state(missoula, montana)).
fof(same_state_ws_butte, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(stpierre_not_montana, axiom, ~in_state(st_pierre, montana)).
fof(any_city_in_butte_not_stpierre, axiom, ! [C,S] : ((in_state(C,S) & in_state(butte,S)) => ~in_state(C, st_pierre))).
fof(uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2)).
fof(goal, conjecture, ~in_state(missoula, montana)).