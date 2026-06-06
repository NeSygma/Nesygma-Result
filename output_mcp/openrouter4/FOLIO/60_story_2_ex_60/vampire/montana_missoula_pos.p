% Positive version: conjecture is "Montana is home to Missoula"
% i.e., in_state(missoula, montana)

% Distinct city names (all named cities are pairwise distinct)
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
     white_sulphur_springs != st_pierre &
     white_sulphur_springs != bristol & white_sulphur_springs != texarkana &
     white_sulphur_springs != texhoma & white_sulphur_springs != union_city &
     st_pierre != bristol & st_pierre != texarkana &
     st_pierre != texhoma & st_pierre != union_city &
     bristol != texarkana & bristol != texhoma & bristol != union_city &
     texarkana != texhoma & texarkana != union_city &
     texhoma != union_city)).

% Premise 1: Billings is a city in the state of Montana in U.S.
fof(premise_1, axiom, in_state(billings, montana)).

% Premise 2: The state of Montana includes the cities of Butte, Helena, and Missoula.
fof(premise_2, axiom,
    (in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana))).

% Premise 3: White Sulphur Springs and Butte are cities in the same state in U.S.
fof(premise_3, axiom,
    ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).

% Premise 4: The city of St Pierre is not in the state of Montana.
fof(premise_4, axiom, ~in_state(st_pierre, montana)).

% Premise 5: Any city in Butte is not in St Pierre.
% Interpreted as: Butte and St Pierre are distinct cities.
% (Already covered by distinctness axiom above, but stated explicitly)
fof(premise_5, axiom, butte != st_pierre).

% Premise 6: A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.
fof(exception_bristol, axiom, exception_city(bristol)).
fof(exception_texarkana, axiom, exception_city(texarkana)).
fof(exception_texhoma, axiom, exception_city(texhoma)).
fof(exception_union_city, axiom, exception_city(union_city)).

fof(one_state_per_city, axiom,
    ! [C, S1, S2] :
        ((in_state(C, S1) & in_state(C, S2) & ~exception_city(C)) => S1 = S2)).

% Conjecture: Montana is home to the city of Missoula.
fof(conjecture, conjecture, in_state(missoula, montana)).