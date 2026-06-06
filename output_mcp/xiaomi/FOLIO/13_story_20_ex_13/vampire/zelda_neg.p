fof(game_decl, axiom, game(legend_of_zelda)).

% Premise 1: A Japanese game company created Legend of Zelda
fof(premise_1, axiom, 
    ? [C] : (japanese_company(C) & created(C, legend_of_zelda))).

% Premise 2: All games on the Top 10 list are made by Japanese game companies
fof(premise_2, axiom,
    ! [G] : ((game(G) & top_10(G)) => 
             ? [C] : (japanese_company(C) & created(C, G)))).

% Premise 3: If a game sells more than one million copies, then it will be included in the Top 10 list
fof(premise_3, axiom,
    ! [G] : ((game(G) & sold_over_million(G)) => top_10(G))).

% Premise 4: The Legend of Zelda sold more than one million copies
fof(premise_4, axiom, sold_over_million(legend_of_zelda)).

% Negated conclusion: The Legend of Zelda is NOT on the Top 10 list
fof(goal, conjecture, ~top_10(legend_of_zelda)).