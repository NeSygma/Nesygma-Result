fof(p1, axiom, in_state(billings, montana)).
fof(p2, axiom, (in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana))).
fof(p3, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(p4, axiom, ~in_state(st_pierre, montana)).
fof(p6, axiom, ! [C, S1, S2] : ((in_state(C, S1) & in_state(C, S2) & S1 != S2) => (C = bristol | C = texarkana | C = texhoma | C = union_city))).
fof(goal, conjecture, ~in_state(missoula, montana)).