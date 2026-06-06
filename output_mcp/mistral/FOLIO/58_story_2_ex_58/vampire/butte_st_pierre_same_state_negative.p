fof(city_in_billings, axiom, city_in(billings, montana)).
fof(city_in_montana_cities, axiom, city_in(butte, montana) & city_in(helena, montana) & city_in(missoula, montana)).
fof(white_sulphur_springs_same_state_as_butte, axiom, ? [State] : (city_in(white_sulphur_springs, State) & city_in(butte, State))).
fof(st_pierre_not_in_montana, axiom, ~city_in(st_pierre, montana)).
fof(butte_not_same_state_as_st_pierre, axiom, ~same_state(butte, st_pierre)).
fof(exceptional_cities, axiom, exceptional_city(bristol) | exceptional_city(texarkana) | exceptional_city(texhoma) | exceptional_city(union_city)).
fof(unique_state_for_normal_cities, axiom,
    ! [City, State1, State2] :
      ((city_in(City, State1) & city_in(City, State2)) =>
       (State1 = State2 | exceptional_city(City)))).

fof(same_state_def, axiom, ! [City1, City2] : (same_state(City1, City2) <=> ? [State] : (city_in(City1, State) & city_in(City2, State)))).

fof(distinct_cities, axiom,
    billings != butte & billings != helena & billings != missoula &
    billings != white_sulphur_springs & billings != st_pierre &
    butte != helena & butte != missoula & butte != white_sulphur_springs &
    butte != st_pierre & helena != missoula & helena != white_sulphur_springs &
    helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre &
    white_sulphur_springs != st_pierre).

fof(conclusion_negation, conjecture, ~same_state(butte, st_pierre)).