fof(city_billings, axiom, city(billings)).
fof(in_state_billings, axiom, in_state(billings, montana)).
fof(city_butte, axiom, city(butte)).
fof(city_helena, axiom, city(helena)).
fof(city_missoula, axiom, city(missoula)).
fof(in_state_butte, axiom, in_state(butte, montana)).
fof(in_state_helena, axiom, in_state(helena, montana)).
fof(in_state_missoula, axiom, in_state(missoula, montana)).
fof(state_montana, axiom, state(montana)).
fof(premise3, axiom, ? [S] : (state(S) & in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(premise4, axiom, ~in_state(st_pierre, montana)).
fof(exception_cities, axiom, (exception(bristol) & exception(texarkana) & exception(texhoma) & exception(union_city))).
fof(unique_state, axiom, ! [C, S1, S2] : ((in_state(C, S1) & in_state(C, S2)) => S1 = S2)).
fof(goal, conjecture, ? [S] : (in_state(butte, S) & in_state(st_pierre, S))).