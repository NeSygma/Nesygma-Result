fof(p1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(p2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(p3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(p4, axiom, ! [X] : (product_of_bbm(X) => cupcake(X))).
fof(p5, axiom, (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies))).
fof(goal, conjecture, (cupcake(dried_thai_chilies) & product_of_bbm(dried_thai_chilies))).