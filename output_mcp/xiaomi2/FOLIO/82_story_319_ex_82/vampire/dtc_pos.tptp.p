fof(p1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(p2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(p3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(p4, axiom, ! [X] : (product_of_bbm(X) => cupcake(X))).
fof(p5, axiom, spicy(dtc) | mala_hotpot(dtc) | ~baked_sweet(dtc)).
fof(goal, conjecture, ~product_of_bbm(dtc) & ~baked_sweet(dtc)).