% Negative version: Conjecture is "St Pierre and Bismarck are NOT in the same state"
fof(distinct_cities, axiom, (
    billings != butte & billings != helena & billings != missoula &
    billings != white_sulphur_springs & billings != st_pierre & billings != bismarck &
    butte != helena & butte != missoula & butte != white_sulphur_springs &
    butte != st_pierre & butte != bismarck &
    helena != missoula & helena != white_sulphur_springs &
    helena != st_pierre & helena != bismarck &
    missoula != white_sulphur_springs & missoula != st_pierre & missoula != bismarck &
    white_sulphur_springs != st_pierre & white_sulphur_springs != bismarck &
    st_pierre != bismarck
)).

% Predicate: city_in_state(City, State)
fof(fact1, axiom, city_in_state(billings, montana)).
fof(fact2, axiom, city_in_state(butte, montana)).
fof(fact3, axiom, city_in_state(helena, montana)).
fof(fact4, axiom, city_in_state(missoula, montana)).

% White Sulphur Springs and Butte are cities in the same state in U.S.
fof(fact5, axiom, ? [S] : (city_in_state(white_sulphur_springs, S) & city_in_state(butte, S))).

% The city of St Pierre is not in the state of Montana.
fof(fact6, axiom, ~city_in_state(st_pierre, montana)).

% A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.
fof(one_state_per_city, axiom, ! [C, S1, S2] : (
    (city_in_state(C, S1) & city_in_state(C, S2)) => S1 = S2
)).

% Negated conclusion: St Pierre and Bismarck are NOT in the same state.
fof(goal_neg, conjecture, ~? [S] : (city_in_state(st_pierre, S) & city_in_state(bismarck, S))).