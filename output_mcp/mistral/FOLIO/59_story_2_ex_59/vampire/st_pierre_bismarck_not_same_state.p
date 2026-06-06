fof(billings_in_montana, axiom, city_in_state(billings, montana)).
fof(butte_in_montana, axiom, city_in_state(butte, montana)).
fof(helena_in_montana, axiom, city_in_state(helena, montana)).
fof(missoula_in_montana, axiom, city_in_state(missoula, montana)).
fof(white_sulphur_springs_same_as_butte, axiom, same_state(white_sulphur_springs, butte)).
fof(st_pierre_not_in_montana, axiom, ~city_in_state(st_pierre, montana)).
fof(butte_not_same_state_as_st_pierre, axiom, ~same_state(butte, st_pierre)).

fof(city_single_state_rule, axiom, 
    ! [C, S1, S2] : 
      ( (C != bristol & C != texarkana & C != texhoma & C != union_city) 
        => ( (city_in_state(C, S1) & city_in_state(C, S2)) => S1 = S2 ) ) ).

fof(conclusion_negation, conjecture, ~same_state(st_pierre, bismarck)).