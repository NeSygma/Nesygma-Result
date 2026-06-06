fof(distinct, axiom, legend_of_zelda != fifa_22).
fof(premise1, axiom, ? [C] : (japanese_company(C) & created(C, legend_of_zelda))).
fof(premise1b, axiom, ! [C, G] : ((japanese_company(C) & created(C, G)) => made_by_japanese(G))).
fof(premise2, axiom, ! [G] : (top_10(G) => made_by_japanese(G))).
fof(premise3, axiom, ! [G] : (big_seller(G) => top_10(G))).
fof(premise4, axiom, big_seller(legend_of_zelda)).
fof(conclusion, conjecture, ~made_by_japanese(fifa_22)).