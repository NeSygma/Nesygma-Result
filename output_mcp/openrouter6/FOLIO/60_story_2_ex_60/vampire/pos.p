% Positive TPTP file: conclusion is true
fof(distinct_constants, axiom,
    (billings != montana & billings != butte & billings != helena & billings != missoula &
     billings != white_sulphur_springs & billings != st_pierre & billings != bristol &
     billings != texarkana & billings != texhoma & billings != union_city &
     montana != butte & montana != helena & montana != missoula &
     montana != white_sulphur_springs & montana != st_pierre & montana != bristol &
     montana != texarkana & montana != texhoma & montana != union_city &
     butte != helena & butte != missoula & butte != white_sulphur_springs &
     butte != st_pierre & butte != bristol & butte != texarkana & butte != texhoma &
     butte != union_city &
     helena != missoula & helena != white_sulphur_springs & helena != st_pierre &
     helena != bristol & helena != texarkana & helena != texhoma & helena != union_city &
     missoula != white_sulphur_springs & missoula != st_pierre & missoula != bristol &
     missoula != texarkana & missoula != texhoma & missoula != union_city &
     white_sulphur_springs != st_pierre & white_sulphur_springs != bristol &
     white_sulphur_springs != texarkana & white_sulphur_springs != texhoma &
     white_sulphur_springs != union_city &
     st_pierre != bristol & st_pierre != texarkana & st_pierre != texhoma &
     st_pierre != union_city &
     bristol != texarkana & bristol != texhoma & bristol != union_city &
     texarkana != texhoma & texarkana != union_city &
     texhoma != union_city)).

fof(premise_1, axiom, city_in_state(billings, montana)).
fof(premise_2a, axiom, city_in_state(butte, montana)).
fof(premise_2b, axiom, city_in_state(helena, montana)).
fof(premise_2c, axiom, city_in_state(missoula, montana)).
fof(premise_3, axiom, city_in_state(white_sulphur_springs, montana)).
fof(premise_4, axiom, ~city_in_state(st_pierre, montana)).
fof(premise_5, axiom, ! [X] : (city_in_state(X, montana) => X != st_pierre)).
fof(exception_def, axiom, ! [X] : (exception(X) <=> (X = bristol | X = texarkana | X = texhoma | X = union_city))).
fof(premise_6, axiom, ! [X] : (exception(X) | ? [S] : (city_in_state(X, S) & ! [S2] : (city_in_state(X, S2) => S2 = S)))).

fof(conclusion, conjecture, city_in_state(missoula, montana)).