% Entities: cities and states
% Predicate: city_in_state(City, State)

% Premise 1: Billings is a city in the state of Montana in U.S.
fof(p1, axiom, city_in_state(billings, montana)).

% Premise 2: The state of Montana includes the cities of Butte, Helena, and Missoula.
fof(p2a, axiom, city_in_state(butte, montana)).
fof(p2b, axiom, city_in_state(helena, montana)).
fof(p2c, axiom, city_in_state(missoula, montana)).

% Premise 3: White Sulphur Springs and Butte are cities in the same state in U.S.
fof(p3, axiom, ? [S] : (city_in_state(white_sulphur_springs, S) & city_in_state(butte, S))).

% Premise 4: The city of St Pierre is not in the state of Montana.
fof(p4, axiom, ~city_in_state(st_pierre, montana)).

% Premise 5: Any city in Butte is not in St Pierre.
% Meaning: any city sharing a state with Butte does not share a state with St Pierre.
fof(p5, axiom, ! [C, S1, S2] :
    ((city_in_state(butte, S1) & city_in_state(C, S1) & city_in_state(st_pierre, S2))
     => ~city_in_state(C, S2))).

% Premise 6: A city can only be in one state except Bristol, Texarkana, Texhoma, Union City.
fof(p6, axiom, ! [C, S1, S2] :
    ((city_in_state(C, S1) & city_in_state(C, S2) &
      C != bristol & C != texarkana & C != texhoma & C != union_city)
     => S1 = S2)).

% Unique Name Assumption: all named entities are distinct
fof(distinct_cities, axiom, (
    billings != butte & billings != helena & billings != missoula &
    billings != white_sulphur_springs & billings != st_pierre &
    billings != bristol & billings != texarkana & billings != texhoma & billings != union_city &
    butte != helena & butte != missoula & butte != white_sulphur_springs &
    butte != st_pierre & butte != bristol & butte != texarkana & butte != texhoma & butte != union_city &
    helena != missoula & helena != white_sulphur_springs & helena != st_pierre &
    helena != bristol & helena != texarkana & helena != texhoma & helena != union_city &
    missoula != white_sulphur_springs & missoula != st_pierre &
    missoula != bristol & missoula != texarkana & missoula != texhoma & missoula != union_city &
    white_sulphur_springs != st_pierre & white_sulphur_springs != bristol &
    white_sulphur_springs != texarkana & white_sulphur_springs != texhoma & white_sulphur_springs != union_city &
    st_pierre != bristol & st_pierre != texarkana & st_pierre != texhoma & st_pierre != union_city &
    bristol != texarkana & bristol != texhoma & bristol != union_city &
    texarkana != texhoma & texarkana != union_city &
    texhoma != union_city
)).

% Montana is distinct from all city names
fof(distinct_state, axiom, (
    montana != billings & montana != butte & montana != helena & montana != missoula &
    montana != white_sulphur_springs & montana != st_pierre &
    montana != bristol & montana != texarkana & montana != texhoma & montana != union_city
)).

% Conclusion: Montana is home to the city of Missoula.
fof(goal, conjecture, city_in_state(missoula, montana)).