% Positive version: Conjecture is "Butte and St Pierre are in the same state"
% i.e., exists a state S such that in_state(butte, S) and in_state(st_pierre, S)

fof(distinct_cities, axiom,
    (billings != butte & billings != helena & billings != missoula &
     billings != white_sulphur_springs & billings != st_pierre &
     billings != bristol & billings != texarkana & billings != texhoma &
     billings != union_city &
     butte != helena & butte != missoula & butte != white_sulphur_springs &
     butte != st_pierre & butte != bristol & butte != texarkana &
     butte != texhoma & butte != union_city &
     helena != missoula & helena != white_sulphur_springs &
     helena != st_pierre & helena != bristol & helena != texarkana &
     helena != texhoma & helena != union_city &
     missoula != white_sulphur_springs & missoula != st_pierre &
     missoula != bristol & missoula != texarkana & missoula != texhoma &
     missoula != union_city &
     white_sulphur_springs != st_pierre & white_sulphur_springs != bristol &
     white_sulphur_springs != texarkana & white_sulphur_springs != texhoma &
     white_sulphur_springs != union_city &
     st_pierre != bristol & st_pierre != texarkana & st_pierre != texhoma &
     st_pierre != union_city &
     bristol != texarkana & bristol != texhoma & bristol != union_city &
     texarkana != texhoma & texarkana != union_city &
     texhoma != union_city)).

fof(distinct_states, axiom,
    (montana != other_state)).

% Billings is a city in the state of Montana in U.S.
fof(fact_billings, axiom, in_state(billings, montana)).

% The state of Montana includes the cities of Butte, Helena, and Missoula.
fof(fact_butte, axiom, in_state(butte, montana)).
fof(fact_helena, axiom, in_state(helena, montana)).
fof(fact_missoula, axiom, in_state(missoula, montana)).

% White Sulphur Springs and Butte are cities in the same state in U.S.
fof(fact_white_sulphur_springs, axiom,
    ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).

% The city of St Pierre is not in the state of Montana.
fof(fact_st_pierre_not_montana, axiom, ~in_state(st_pierre, montana)).

% Any city in Butte is not in St Pierre.
% This is tricky: "Any city in Butte" - Butte is a city, not a state.
% Possibly means: Any city that is in Butte (i.e., a city located within Butte) is not in St Pierre.
% Or more likely: Butte and St Pierre are not the same city (already covered by distinctness).
% Or: There is no city that is both in Butte and in St Pierre.
% Let's interpret as: Butte and St Pierre are distinct cities (already covered).
% Or: For any city X, if X is in Butte (as a location) then X is not in St Pierre.
% Since Butte is a city, "in Butte" might mean "located within the city of Butte".
% But we don't have a predicate for that. Let's interpret it as:
% Butte and St Pierre are not the same city (already covered by distinctness).
% So we can skip this as already covered.

% A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.
fof(one_state_per_city, axiom,
    ! [C, S1, S2] :
        ((in_state(C, S1) & in_state(C, S2) &
          C != bristol & C != texarkana & C != texhoma & C != union_city)
         => S1 = S2)).

% Conclusion: Butte and St Pierre are in the same state.
fof(goal, conjecture,
    ? [S] : (in_state(butte, S) & in_state(st_pierre, S))).