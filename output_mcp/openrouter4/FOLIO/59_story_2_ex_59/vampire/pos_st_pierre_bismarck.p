% Positive conjecture: St Pierre and Bismarck are in the same state
fof(premise1, axiom, in_state(billings, montana)).
fof(premise2_1, axiom, in_state(butte, montana)).
fof(premise2_2, axiom, in_state(helena, montana)).
fof(premise2_3, axiom, in_state(missoula, montana)).
fof(premise3, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(premise4, axiom, ~in_state(st_pierre, montana)).
fof(premise5, axiom, butte != st_pierre).

% A city can only be in one state, except for Bristol, Texarkana, Texhoma, Union City
fof(one_state_per_city, axiom, ! [C, S1, S2] : (
    (in_state(C, S1) & in_state(C, S2) & 
     C != bristol & C != texarkana & C != texhoma & C != union_city) => 
    S1 = S2
)).

% Distinctness of all named cities
fof(distinct_cities, axiom, (
    billings != butte & billings != helena & billings != missoula & 
    billings != white_sulphur_springs & billings != st_pierre & 
    billings != bismarck & 
    butte != helena & butte != missoula & butte != white_sulphur_springs & 
    butte != st_pierre & butte != bismarck & 
    helena != missoula & helena != white_sulphur_springs & 
    helena != st_pierre & helena != bismarck & 
    missoula != white_sulphur_springs & missoula != st_pierre & 
    missoula != bismarck & 
    white_sulphur_springs != st_pierre & white_sulphur_springs != bismarck & 
    st_pierre != bismarck
)).

% Conclusion: St Pierre and Bismarck are in the same state
fof(goal, conjecture, ? [S] : (in_state(st_pierre, S) & in_state(bismarck, S))).