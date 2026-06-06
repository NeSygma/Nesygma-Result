% Positive version: original conclusion as conjecture
fof(premise1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise4, axiom, ! [X] : (product_from_baked_by_melissa(X) => cupcake(X))).
fof(premise5, axiom, (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies))).
fof(conclusion, conjecture, (~product_from_baked_by_melissa(dried_thai_chilies) & ~baked_sweet(dried_thai_chilies))).