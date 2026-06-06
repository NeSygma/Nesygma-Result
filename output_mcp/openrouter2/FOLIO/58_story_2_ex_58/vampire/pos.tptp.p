fof(billings_in_montana, axiom, in_state(billings, montana)).
fof(butte_in_montana, axiom, in_state(butte, montana)).
fof(helena_in_montana, axiom, in_state(helena, montana)).
fof(missoula_in_montana, axiom, in_state(missoula, montana)).
fof(white_sulphur_springs_butte_same, axiom, same_state(white_sulphur_springs, butte)).
fof(st_pierre_not_in_montana, axiom, ~in_state(st_pierre, montana)).
fof(butte_not_same_st_pierre, axiom, ~same_state(butte, st_pierre)).
fof(distinct_exceptions, axiom, (bristol != texarkana & bristol != texhoma & bristol != union_city & texarkana != texhoma & texarkana != union_city & texhoma != union_city)).
fof(unique_state, axiom, ! [X,S1,S2] : ((in_state(X,S1) & in_state(X,S2) & X != bristol & X != texarkana & X != texhoma & X != union_city) => S1 = S2)).
fof(same_state_def1, axiom, ! [X,Y] : (same_state(X,Y) => ? [S] : (in_state(X,S) & in_state(Y,S)))).
fof(same_state_def2, axiom, ! [X,Y,S] : (in_state(X,S) & in_state(Y,S) => same_state(X,Y))).
fof(conjecture, conjecture, same_state(butte, st_pierre)).