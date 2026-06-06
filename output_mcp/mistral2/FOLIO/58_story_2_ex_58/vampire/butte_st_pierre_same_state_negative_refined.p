fof(city_in_billings_montana, axiom, city_in(billings, montana)).
fof(city_in_butte_montana, axiom, city_in(butte, montana)).
fof(city_in_helena_montana, axiom, city_in(helena, montana)).
fof(city_in_missoula_montana, axiom, city_in(missoula, montana)).
fof(city_in_white_sulphur_springs_montana, axiom, city_in(white_sulphur_springs, montana)).
fof(same_state_white_sulphur_butte, axiom, same_state(white_sulphur_springs, butte)).
fof(st_pierre_not_in_montana, axiom, ~city_in(st_pierre, montana)).
fof(butte_not_in_st_pierre, axiom, ~city_in(butte, st_pierre)).
fof(distinct_cities, axiom, billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre).
fof(distinct_states, axiom, montana != st_pierre).

fof(def_same_state, axiom, ! [C1, C2, S] : (same_state(C1, C2) <=> (city_in(C1, S) & city_in(C2, S)))).

fof(exception_cities, axiom, (bristol = bristol & texarkana = texarkana & texhoma = texhoma & union_city = union_city)).

fof(conclusion_negation, conjecture, ~same_state(butte, st_pierre)).