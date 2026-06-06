fof(city_billings, axiom, city(billings)).
fof(state_montana, axiom, state(montana)).
fof(billings_in_montana, axiom, in_state(billings, montana)).

% Premise 2: Montana includes Butte, Helena, Missoula
fof(city_butte, axiom, city(butte)).
fof(city_helena, axiom, city(helena)).
fof(city_missoula, axiom, city(missoula)).
fof(butte_in_montana, axiom, in_state(butte, montana)).
fof(helena_in_montana, axiom, in_state(helena, montana)).
fof(missoula_in_montana, axiom, in_state(missoula, montana)).

% Premise 3: White Sulphur Springs and Butte are in the same state
fof(city_wss, axiom, city(white_sulphur_springs)).
fof(wss_same_state_as_butte, axiom,
    ? [S] : (state(S) & in_state(white_sulphur_springs, S) & in_state(butte, S))).

% Premise 4: St Pierre is not in Montana
fof(city_st_pierre, axiom, city(st_pierre)).
fof(st_pierre_not_montana, axiom, ~in_state(st_pierre, montana)).

% Premise 5: Any city in Butte's state is not in St Pierre's state
fof(butte_state_not_st_pierre_state, axiom,
    ! [S] : (in_state(butte, S) => ~in_state(st_pierre, S))).

% Premise 6: Single state constraint (except Bristol, Texarkana, Texhoma, Union City)
fof(city_bristol, axiom, city(bristol)).
fof(city_texarkana, axiom, city(texarkana)).
fof(city_texhoma, axiom, city(texhoma)).
fof(city_union_city, axiom, city(union_city)).
fof(single_state, axiom,
    ! [X, S1, S2] :
        ((city(X) & X != bristol & X != texarkana & X != texhoma & X != union_city &
          in_state(X, S1) & in_state(X, S2)) => S1 = S2)).

% Declare Bismarck as a city (referenced in conclusion)
fof(city_bismarck, axiom, city(bismarck)).

% Unique Name Assumption for all constants
fof(una, axiom, (
    billings != butte & billings != helena & billings != missoula &
    billings != white_sulphur_springs & billings != st_pierre & billings != bismarck &
    billings != bristol & billings != texarkana & billings != texhoma & billings != union_city &
    butte != helena & butte != missoula & butte != white_sulphur_springs &
    butte != st_pierre & butte != bismarck &
    butte != bristol & butte != texarkana & butte != texhoma & butte != union_city &
    helena != missoula & helena != white_sulphur_springs & helena != st_pierre &
    helena != bismarck &
    helena != bristol & helena != texarkana & helena != texhoma & helena != union_city &
    missoula != white_sulphur_springs & missoula != st_pierre & missoula != bismarck &
    missoula != bristol & missoula != texarkana & missoula != texhoma & missoula != union_city &
    white_sulphur_springs != st_pierre & white_sulphur_springs != bismarck &
    white_sulphur_springs != bristol & white_sulphur_springs != texarkana &
    white_sulphur_springs != texhoma & white_sulphur_springs != union_city &
    st_pierre != bismarck &
    st_pierre != bristol & st_pierre != texarkana & st_pierre != texhoma & st_pierre != union_city &
    bismarck != bristol & bismarck != texarkana & bismarck != texhoma & bismarck != union_city &
    bristol != texarkana & bristol != texhoma & bristol != union_city &
    texarkana != texhoma & texarkana != union_city &
    texhoma != union_city
)).

% Conclusion: St Pierre and Bismarck are in the same state
fof(goal, conjecture,
    ? [S] : (in_state(st_pierre, S) & in_state(bismarck, S))).