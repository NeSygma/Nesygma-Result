fof(premise1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise4, axiom, ! [X] : (baked_by_melissa(X) => cupcake(X))).
fof(premise5, axiom, spicy(dtc) | mala_hotpot(dtc) | ~baked_sweet(dtc)).
fof(conclusion, conjecture, ~baked_by_melissa(dtc)).