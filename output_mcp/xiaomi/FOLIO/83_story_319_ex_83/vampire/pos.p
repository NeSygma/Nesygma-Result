fof(premise_1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise_2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise_3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise_4, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).
fof(premise_5, axiom, (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies))).
fof(goal, conjecture, (cupcake(dried_thai_chilies) & product_of_baked_by_melissa(dried_thai_chilies))).