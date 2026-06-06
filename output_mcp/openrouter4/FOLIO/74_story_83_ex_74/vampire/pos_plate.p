fof(premise1, axiom, ! [X] : (istanbul_plate(X) => begins_with_34(X))).
fof(premise2, axiom, ! [X] : (~begins_with_34(X) => ~istanbul_plate(X))).
fof(premise3, axiom, istanbul_plate(joes_plate)).
fof(premise4, axiom, begins_with_35(toms_plate)).
fof(premise5, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).
fof(goal, conjecture, begins_with_34(joes_plate)).