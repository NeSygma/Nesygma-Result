% Positive version: prove not product_of_bm(dried_thai_chilies)
fof(ax1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(ax2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(ax3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(ax4, axiom, ! [X] : (product_of_bm(X) => cupcake(X))).
fof(ax5, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).
fof(conj, conjecture, ~product_of_bm(dried_thai_chilies)).