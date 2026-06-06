fof(premise_1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise_2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise_3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise_4, axiom, ! [X] : (baked_by_melissa(X) => cupcake(X))).
fof(premise_5, axiom, (spicy(dtc) | mala_hotpot(dtc) | ~baked_sweet(dtc))).
fof(goal, conjecture, ~mala_hotpot(dtc)).