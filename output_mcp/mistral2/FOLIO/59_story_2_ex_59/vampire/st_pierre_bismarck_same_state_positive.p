fof(city_in_billings, axiom, city_in(billings, montana)).
fof(city_in_butte, axiom, city_in(butte, montana)).
fof(city_in_helena, axiom, city_in(helena, montana)).
fof(city_in_missoula, axiom, city_in(missoula, montana)).
fof(city_in_white_sulphur_springs, axiom, city_in(white_sulphur_springs, montana)).
fof(city_in_st_pierre_not_montana, axiom, city_in(st_pierre, other_state)).
fof(butte_and_st_pierre_not_same_state, axiom, ! [S] : ~(city_in(butte, S) & city_in(st_pierre, S))).
fof(unique_state_for_cities, axiom, 
    ! [C, S1, S2] : 
      ((city_in(C, S1) & city_in(C, S2) & ~exception_city(C)) 
       => (S1 = S2))).
fof(exception_city_definition, axiom, 
    exception_city(bristol) | exception_city(texarkana) | exception_city(texhoma) | exception_city(union_city)).
fof(same_state_definition, axiom, 
    ! [C1, C2, S] : (same_state(C1, C2, S) <=> (city_in(C1, S) & city_in(C2, S)))).

fof(conclusion, conjecture, ? [S] : same_state(st_pierre, bismarck, S)).