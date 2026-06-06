% Negative version
fof(billings_montana, axiom, in_state(billings, montana)).
fof(butte_montana, axiom, in_state(butte, montana)).
fof(helena_montana, axiom, in_state(helena, montana)).
fof(missoula_montana, axiom, in_state(missoula, montana)).
fof(white_butte_same_state, axiom, ?[S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(stpierre_not_montana, axiom, ~in_state(st_pierre, montana)).
fof(butte_excludes_stpierre, axiom, ![S] : (in_state(butte, S) => ~in_state(st_pierre, S))).
fof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)).
fof(goal_neg, conjecture, ![S] : (in_state(butte, S) => ~in_state(st_pierre, S))).