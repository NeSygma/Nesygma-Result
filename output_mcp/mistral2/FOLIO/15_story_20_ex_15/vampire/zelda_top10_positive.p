fof(premise_1, axiom, japanese_game_company(the_legend_of_zelda)).
fof(premise_2, axiom, ! [G] : (top_10_list(G) => japanese_game_company(G))).
fof(premise_3, axiom, ! [G] : (sells_more_than_one_million(G) => top_10_list(G))).
fof(premise_4, axiom, sells_more_than_one_million(the_legend_of_zelda)).
fof(conclusion, conjecture, ~top_10_list(the_legend_of_zelda)).