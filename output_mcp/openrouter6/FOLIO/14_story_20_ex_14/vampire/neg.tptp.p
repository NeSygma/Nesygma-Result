fof(premise1, axiom, ? [C] : (japanese_company(C) & created(C, legend_of_zelda))).
fof(legend_is_game, axiom, game(legend_of_zelda)).
fof(premise2, axiom, ! [G] : (top10(G) => ? [C] : (japanese_company(C) & created(C, G)))).
fof(premise3, axiom, ! [G] : (sells_more_than_million(G) => top10(G))).
fof(premise4, axiom, sells_more_than_million(legend_of_zelda)).
fof(distinct_games, axiom, legend_of_zelda != fifa22).
fof(neg_conclusion, conjecture, ~? [C] : (japanese_company(C) & created(C, fifa22))).