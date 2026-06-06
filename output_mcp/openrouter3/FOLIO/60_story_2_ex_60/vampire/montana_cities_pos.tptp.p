% Problem: Montana cities reasoning
% Positive version: Montana is home to Missoula (conjecture)

% Entities
fof(distinct_cities, axiom, 
    (billings != butte & billings != helena & billings != missoula & 
     billings != white_sulphur_springs & billings != st_pierre &
     butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre &
     helena != missoula & helena != white_sulphur_springs & helena != st_pierre &
     missoula != white_sulphur_springs & missoula != st_pierre &
     white_sulphur_springs != st_pierre)).

fof(distinct_exception_cities, axiom,
    (bristol != texarkana & bristol != texhoma & bristol != union_city &
     texarkana != texhoma & texarkana != union_city &
     texhoma != union_city)).

% States
fof(montana_is_state, axiom, state(montana)).

% Premise 1: Billings is a city in Montana in U.S.
fof(premise_1, axiom, city_in_state(billings, montana)).

% Premise 2: Montana includes Butte, Helena, Missoula
fof(premise_2a, axiom, city_in_state(butte, montana)).
fof(premise_2b, axiom, city_in_state(helena, montana)).
fof(premise_2c, axiom, city_in_state(missoula, montana)).

% Premise 3: White Sulphur Springs and Butte are in the same state in U.S.
fof(premise_3, axiom, ? [S] : (city_in_state(white_sulphur_springs, S) & city_in_state(butte, S))).

% Premise 4: St Pierre is not in Montana
fof(premise_4, axiom, ~city_in_state(st_pierre, montana)).

% Premise 5: Any city in Butte's state is not in St Pierre's state
% Interpretation: If a city is in the same state as Butte, then it's not in the same state as St Pierre
fof(premise_5, axiom, 
    ! [C, S1, S2] : 
        ((city_in_state(C, S1) & city_in_state(butte, S1) & city_in_state(st_pierre, S2)) 
         => ~city_in_state(C, S2))).

% Premise 6: Uniqueness constraint with exceptions
% For non-exception cities, they can only be in one state
fof(premise_6, axiom,
    ! [C, S1, S2] : 
        ((city_in_state(C, S1) & city_in_state(C, S2) & 
          C != bristol & C != texarkana & C != texhoma & C != union_city)
         => S1 = S2)).

% Conclusion: Montana is home to Missoula
fof(goal, conjecture, city_in_state(missoula, montana)).