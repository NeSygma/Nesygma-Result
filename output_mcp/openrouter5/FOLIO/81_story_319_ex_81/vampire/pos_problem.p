% Positive version: original conclusion as conjecture
% Premises:
% 1. No baked sweets are spicy.
fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
% 2. All cupcakes are baked sweets.
fof(all_cupcakes_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
% 3. All mala hotpots are spicy.
fof(all_mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
% 4. All products from Baked by Melissa are cupcakes.
fof(all_baked_by_melissa_cupcakes, axiom, ! [X] : (baked_by_melissa_product(X) => cupcake(X))).
% 5. Dried Thai chilies are spicy or mala hotpots or not baked sweets.
fof(dried_thai_chilies_prop, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).

% Distinctness (only one named entity)
fof(distinct, axiom, $true).

% Conclusion: Dried Thai chilies are a mala hotpot.
fof(conclusion, conjecture, mala_hotpot(dried_thai_chilies)).