fof(japanese_company_exists, axiom,
    japanese_game_company(nintendo)).

fof(zelda_created, axiom,
    created(nintendo, legend_of_zelda)).

fof(top10_made_by_japanese, axiom,
    ! [G] : (on_top_10_list(G) => made_by_japanese_company(G))).

fof(sold_over_million_top10, axiom,
    ! [G] : (sold_over_million(G) => on_top_10_list(G))).

fof(zelda_sold_million, axiom,
    sold_over_million(legend_of_zelda)).

fof(created_implies_made_by, axiom,
    ! [C, G] : ((japanese_game_company(C) & created(C, G)) => made_by_japanese_company(G))).

fof(goal, conjecture,
    ~made_by_japanese_company(fifa_22)).