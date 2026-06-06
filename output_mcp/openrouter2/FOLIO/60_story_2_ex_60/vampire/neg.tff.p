tff(distinct, axiom, $distinct(billings, butte, helena, missoula, white_sulphur_springs, st_pierre, bristol, texarkana, texhoma, union_city, montana)).
tff(billings_in_montana, axiom, in_state(billings, montana)).
tff(butte_in_montana, axiom, in_state(butte, montana)).
tff(helena_in_montana, axiom, in_state(helena, montana)).
tff(missoula_in_montana, axiom, in_state(missoula, montana)).
tff(white_sulphur_springs_in_montana, axiom, in_state(white_sulphur_springs, montana)).
tff(st_pierre_not_in_montana, axiom, ~in_state(st_pierre, montana)).
tff(butte_not_in_st_pierre, axiom, ~in_state(butte, st_pierre)).
tff(unique_state, axiom, ! [C,S1,S2] : ((C != bristol & C != texarkana & C != texhoma & C != union_city & in_state(C,S1) & in_state(C,S2)) => S1 = S2)).
tff(conjecture, conjecture, ~in_state(missoula, montana)).