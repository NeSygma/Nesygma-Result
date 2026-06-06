fof(axiom_billings_in_montana, axiom, in_state(billings, montana)).
fof(axiom_montana_includes_butte, axiom, in_state(butte, montana)).
fof(axiom_montana_includes_helena, axiom, in_state(helena, montana)).
fof(axiom_montana_includes_missoula, axiom, in_state(missoula, montana)).
fof(axiom_ws_and_butte_same_state, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).
fof(axiom_st_pierre_not_in_montana, axiom, ~ in_state(st_pierre, montana)).
fof(axiom_uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & S1 != S2) => (C = bristol | C = texarkana | C = texhoma | C = union_city))).
fof(negated_conclusion, conjecture, ~ in_state(missoula, montana)).