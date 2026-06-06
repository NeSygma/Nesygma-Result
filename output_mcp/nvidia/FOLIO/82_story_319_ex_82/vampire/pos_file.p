fof(axiom1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(axiom2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(axiom3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(axiom4, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).
fof(axiom5, axiom, spicy(dried_thai_chili) | mala_hotpot(dried_thai_chili) | ~baked_sweet(dried_thai_chili)).
fof(conclusion, conjecture, ~product_of_baked_by_melissa(dried_thai_chili) & ~baked_sweet(dried_thai_chili)).