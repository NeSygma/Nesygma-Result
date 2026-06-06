fof(premise_1, axiom, ? [C] : (japanese_game_company(C) & created_by(C, legend_of_zelda))).
fof(premise_2, axiom, ! [G] : (on_top_10(G) => ? [C] : (japanese_game_company(C) & created_by(C, G)))).
fof(premise_3, axiom, ! [G] : (sold_more_than_one_million(G) => on_top_10(G))).
fof(premise_4, axiom, sold_more_than_one_million(legend_of_zelda)).
fof(conclusion, conjecture, ~on_top_10(legend_of_zelda)).