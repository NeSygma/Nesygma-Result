fof(premise_1, axiom, located_in(beijing, northern_china)).
fof(premise_2, axiom, ! [X] : (located_in(X, northern_china) => ~located_in(X, southern_china))).
fof(goal, conjecture, ~located_in(beijing, southern_china)).