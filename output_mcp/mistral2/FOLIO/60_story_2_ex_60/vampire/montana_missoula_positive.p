fof(city_in_billings_montana, axiom, city_in(billings, montana)).
fof(city_in_butte_montana, axiom, city_in(butte, montana)).
fof(city_in_helena_montana, axiom, city_in(helena, montana)).
fof(city_in_missoula_montana, axiom, city_in(missoula, montana)).
fof(same_state_white_sulphur_butte, axiom, same_state(white_sulphur_springs, butte)).
fof(not_in_state_st_pierre_montana, axiom, not_in_state(st_pierre, montana)).
fof(city_in_butte_implies_not_in_st_pierre, axiom, ! [X] : (city_in(X, butte) => ~city_in(X, st_pierre))).
fof(only_one_state_except, axiom, ! [C, S1, S2] : ((city_in(C, S1) & city_in(C, S2)) => (S1 = S2))).
fof(def_same_state, axiom, ! [X, Y] : (same_state(X, Y) <=> ? [S] : (city_in(X, S) & city_in(Y, S)))).
fof(goal, conjecture, city_in(missoula, montana)).