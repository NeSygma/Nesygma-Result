fof(premise1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise4, axiom, ! [X] : (from_baked_by_melissa(X) => cupcake(X))).
fof(premise5, axiom, spicy(dried_thai_chili) | mala_hotpot(dried_thai_chili) | ~baked_sweet(dried_thai_chili)).
fof(neg_conclusion, conjecture, ~(cupcake(dried_thai_chili) & from_baked_by_melissa(dried_thai_chili))).