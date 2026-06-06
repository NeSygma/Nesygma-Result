% Negative version: Conjecture is "Montana is NOT home to the city of Missoula"
% i.e., ~in_state(missoula, montana)

% Predicate: in_state(City, State) means City is in State
% Constants: billings, butte, helena, missoula, white_sulphur_springs, st_pierre, montana

% Distinctness of cities and states
fof(distinct_cities, axiom, (
    billings != butte & billings != helena & billings != missoula &
    billings != white_sulphur_springs & billings != st_pierre &
    butte != helena & butte != missoula & butte != white_sulphur_springs &
    butte != st_pierre &
    helena != missoula & helena != white_sulphur_springs & helena != st_pierre &
    missoula != white_sulphur_springs & missoula != st_pierre &
    white_sulphur_springs != st_pierre
)).

% Premise 1: Billings is a city in the state of Montana in U.S.
fof(premise1, axiom, in_state(billings, montana)).

% Premise 2: The state of Montana includes the cities of Butte, Helena, and Missoula.
fof(premise2, axiom, 
    (in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana))).

% Premise 3: White Sulphur Springs and Butte are cities in the same state in U.S.
fof(premise3, axiom, 
    ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).

% Premise 4: The city of St Pierre is not in the state of Montana.
fof(premise4, axiom, ~in_state(st_pierre, montana)).

% Premise 5: Any city in Butte is not in St Pierre.
fof(premise5_city, axiom,
    ! [X] : (located_in(X, butte) => ~located_in(X, st_pierre))).

% Premise 6: A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.
fof(premise6, axiom,
    ! [C, S1, S2] : (
        (in_state(C, S1) & in_state(C, S2) & C != bristol & C != texarkana & C != texhoma & C != union_city)
        => S1 = S2
    )).

% Distinctness of exception cities
fof(distinct_exceptions, axiom,
    (bristol != texarkana & bristol != texhoma & bristol != union_city &
     texarkana != texhoma & texarkana != union_city &
     texhoma != union_city)).

% Negated conclusion: Montana is NOT home to the city of Missoula.
fof(neg_conclusion, conjecture, ~in_state(missoula, montana)).