% Positive conjecture: St Pierre and Bismarck are in the same state
fof(city_billings, axiom, city(billings)).
fof(state_montana, axiom, state(montana)).
fof(in_billings_montana, axiom, in_state(billings, montana)).
fof(city_butte, axiom, city(butte)).
fof(city_helena, axiom, city(helena)).
fof(city_missoula, axiom, city(missoula)).
fof(in_butte_montana, axiom, in_state(butte, montana)).
fof(in_helena_montana, axiom, in_state(helena, montana)).
fof(in_missoula_montana, axiom, in_state(missoula, montana)).
fof(city_white_sulphur_springs, axiom, city(white_sulphur_springs)).
% White Sulphur Springs and Butte are cities in the same state
fof(same_state_wss_butte, axiom, ! [S] : (in_state(white_sulphur_springs,S) <=> in_state(butte,S))).
fof(city_st_pierre, axiom, city(st_pierre)).
fof(not_in_montana_st_pierre, axiom, ~in_state(st_pierre, montana)).
fof(city_bismarck, axiom, city(bismarck)).
% Uniqueness of state for each city except exceptions
fof(exceptions, axiom, (bristol != texarkana & bristol != texhoma & bristol != union_city &
                         texarkana != texhoma & texarkana != union_city &
                         texhoma != union_city)).
fof(unique_state, axiom, ! [C,S1,S2] : ((city(C) & in_state(C,S1) & in_state(C,S2) &
                                         C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2)).
% Distinctness of city constants
fof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula &
                            billings != white_sulphur_springs & billings != st_pierre & billings != bismarck &
                            butte != helena & butte != missoula & butte != white_sulphur_springs &
                            butte != st_pierre & butte != bismarck &
                            helena != missoula & helena != white_sulphur_springs & helena != st_pierre & helena != bismarck &
                            missoula != white_sulphur_springs & missoula != st_pierre & missoula != bismarck &
                            white_sulphur_springs != st_pierre & white_sulphur_springs != bismarck &
                            st_pierre != bismarck)).
% Conjecture: there exists a state S such that both St Pierre and Bismarck are in S
fof(goal, conjecture, ? [S] : (in_state(st_pierre,S) & in_state(bismarck,S))).