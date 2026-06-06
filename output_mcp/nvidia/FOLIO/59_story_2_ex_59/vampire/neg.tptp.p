fof(premise1, axiom, in_state(billings, montana)).
fof(premise2a, axiom, in_state(butte, montana)).
fof(premise2b, axiom, in_state(helena, montana)).
fof(premise2c, axiom, in_state(missoula, montana)).
fof(premise3, axiom, ? [S] : (in_state(whitesulphursprings, S) & in_state(butte, S))).
fof(premise4, axiom, ~ in_state(st_pierre, montana)).
fof(premise5, axiom, ~ in_state(butte, st_pierre)).
fof(premise6, axiom, ! [X,S1,S2] : ((in_state(X,S1) & in_state(X,S2) & S1 != S2) => (X = bristol | X = texarkana | X = texhoma | X = unioncity))).
fof(conclusion_neg, conjecture, ! [S] : (~ in_state(st_pierre, S) | ~ in_state(bismarck, S))).