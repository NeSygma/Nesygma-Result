fof(billings_in_mt, axiom, in_state(billings, montana)).
fof(butte_in_mt, axiom, in_state(butte, montana)).
fof(helena_in_mt, axiom, in_state(helena, montana)).
fof(missoula_in_mt, axiom, in_state(missoula, montana)).
fof(wss_and_butte_same_state, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(sp_not_in_mt, axiom, ~in_state(st_pierre, montana)).
fof(butte_not_sp_state, axiom, ~same_state(butte, st_pierre)).
fof(one_state_rule, axiom, ! [C, S1, S2] : ((in_state(C, S1) & in_state(C, S2) & ~is_exception(C)) => S1 = S2)).
fof(exceptions, axiom, (is_exception(bristol) & is_exception(texarkana) & is_exception(texhoma) & is_exception(union_city))).
fof(same_state_def, axiom, ! [C1, C2] : (same_state(C1, C2) <=> ? [S] : (in_state(C1, S) & in_state(C2, S)))).
fof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & billings != bismarck & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & butte != bismarck & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & helena != bismarck & missoula != white_sulphur_springs & missoula != st_pierre & missoula != bismarck & white_sulphur_springs != st_pierre & white_sulphur_springs != bismarck & st_pierre != bismarck)).

fof(goal, conjecture, ~same_state(st_pierre, bismarck)).