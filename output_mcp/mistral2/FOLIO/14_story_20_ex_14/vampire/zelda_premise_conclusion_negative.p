fof(created_zelda, axiom, created_by_japanese_company(legend_of_zelda)).
fof(top_10_implies_japanese, axiom, ! [G] : (top_10(G) => created_by_japanese_company(G))).
fof(sells_implies_top_10, axiom, ! [G] : (sells_more_than_one_million(G) => top_10(G))).
fof(zelda_sells, axiom, sells_more_than_one_million(legend_of_zelda)).
fof(conclusion_negation, conjecture, ~created_by_japanese_company(fifa_22)).