fof(legend_is_game, axiom, game(legend_of_zelda)).

fof(premise1, axiom,
    ? [X] : (japanese_game_company(X) & created(X, legend_of_zelda))).

fof(premise2, axiom,
    ! [G] : ((game(G) & on_top_10_list(G)) =>
        ? [C] : (japanese_game_company(C) & made_by(G, C)))).

fof(premise3, axiom,
    ! [G] : ((game(G) & sold_more_than_one_million(G)) =>
        on_top_10_list(G))).

fof(premise4, axiom,
    sold_more_than_one_million(legend_of_zelda)).

fof(goal, conjecture,
    ~on_top_10_list(legend_of_zelda)).