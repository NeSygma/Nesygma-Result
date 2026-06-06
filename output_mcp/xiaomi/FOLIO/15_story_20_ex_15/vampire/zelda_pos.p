% Entities
fof(legend_of_zelda_is_a_game, axiom, game(legend_of_zelda)).

% Premise 1: A Japanese game company created Legend of Zelda
fof(premise_1, axiom, 
    ? [C] : (japanese_game_company(C) & created(C, legend_of_zelda))).

% Premise 2: All games on the Top 10 list are made by Japanese game companies
fof(premise_2, axiom,
    ! [G] : ((game(G) & on_top_10(G)) => 
             ? [C] : (japanese_game_company(C) & created(C, G)))).

% Premise 3: If a game sells more than 1M copies, it's on the Top 10 list
fof(premise_3, axiom,
    ! [G] : ((game(G) & sold_over_million(G)) => on_top_10(G))).

% Premise 4: Legend of Zelda sold more than 1M copies
fof(premise_4, axiom, sold_over_million(legend_of_zelda)).

% Conclusion: Legend of Zelda is NOT on the Top 10 list
fof(conclusion, conjecture, ~on_top_10(legend_of_zelda)).