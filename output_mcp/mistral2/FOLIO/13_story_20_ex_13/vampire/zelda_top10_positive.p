fof(company_exists, axiom, ? [C] : japanese_game_company(C)).
fof(created_by_zelda, axiom, created_by(the_legend_of_zelda, c1)).
fof(japanese_creator, axiom, japanese_game_company(c1)).
fof(all_top10_japanese, axiom,
    ! [G] : (on_top_10_list(G) => ? [C] : (created_by(G, C) & japanese_game_company(C)))).
fof(sales_to_top10, axiom,
    ! [G] : (sells_more_than_one_million(G) => on_top_10_list(G))).
fof(zelda_sales, axiom, sells_more_than_one_million(the_legend_of_zelda)).
fof(goal, conjecture, on_top_10_list(the_legend_of_zelda)).