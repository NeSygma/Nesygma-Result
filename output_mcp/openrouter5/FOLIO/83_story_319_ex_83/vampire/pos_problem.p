% Positive version: original conclusion as conjecture
% Premises:
% 1. No baked sweets are spicy.
fof(no_baked_sweets_are_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).

% 2. All cupcakes are baked sweets.
fof(all_cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).

% 3. All mala hotpots are spicy.
fof(all_mala_hotpots_are_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).

% 4. All products from Baked by Melissa are cupcakes.
fof(all_baked_by_melissa_are_cupcakes, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).

% 5. Dried Thai chilies are spicy or mala hotpots or not baked sweets.
fof(dried_thai_chilies_property, axiom,
    (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies))).

% Conclusion: Dried Thai chilies are cupcakes and products of Baked by Melissa.
fof(conclusion, conjecture,
    (cupcake(dried_thai_chilies) & product_of_baked_by_melissa(dried_thai_chilies))).