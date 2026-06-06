fof(legend_of_zelda_created_by_japanese, axiom, created_by_japanese_company(legend_of_zelda)).
fof(top_10_implies_japanese, axiom, ! [G] : (on_top_10_list(G) => created_by_japanese_company(G))).
fof(sales_implies_top_10, axiom, ! [G] : (sold_more_than_one_million(G) => on_top_10_list(G))).
fof(legend_of_zelda_sales, axiom, sold_more_than_one_million(legend_of_zelda)).
fof(goal_negation, conjecture, ~created_by_japanese_company(fifa_22)).