% Negative version: negated conclusion as conjecture
% Premises:
% 1. No baked sweets are spicy.
fof(premise1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
% 2. All cupcakes are baked sweets.
fof(premise2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
% 3. All mala hotpots are spicy.
fof(premise3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
% 4. All products from Baked by Melissa are cupcakes.
fof(premise4, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).
% 5. Dried Thai chilies are spicy or mala hotpots or not baked sweets.
fof(premise5_corrected, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).

% Negated conclusion: Dried Thai chilies are NOT products of Baked by Melissa.
fof(neg_conclusion, conjecture, ~product_of_baked_by_melissa(dried_thai_chilies)).