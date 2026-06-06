fof(billings_city, axiom, in_state(billings, montana)).
fof(montana_state, axiom, state(montana)).
fof(butte_in_montana, axiom, in_state(butte, montana)).
fof(helena_in_montana, axiom, in_state(helena, montana)).
fof(missoula_in_montana, axiom, in_state(missoula, montana)).
fof(whitesprings_city, axiom, city(whitesprings)).
fof(butte_city, axiom, city(butte)).
fof(whitesprings_and_butte_same_state, axiom, ? [S] : (in_state(whitesprings, S) & in_state(butte, S))).
fof(st_pierre_not_montana, axiom, ~in_state(st_pierre, montana)).
fof(any_city_not_in_st_pierre, axiom, ! [X] : (in_state(X, montana) => ~in_state(X, st_pierre))).
fof(uniqueness, axiom, ! [X,S1,S2] : ((in_state(X,S1) & in_state(X,S2) & X != Bristol & X != Texarkana & X != Texhoma & X != UnionCity) => S1 = S2)).
fof(goal, conjecture, ! [S] : (~in_state(butte, S) | ~in_state(st_pierre, S))).