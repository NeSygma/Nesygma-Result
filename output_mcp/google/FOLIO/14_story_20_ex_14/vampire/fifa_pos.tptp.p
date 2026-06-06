fof(p1, axiom, ? [C] : (japanese_game_company(C) & created_by(C, legend_of_zelda))).
fof(p2, axiom, ! [G] : (in_top_10(G) => ? [C] : (japanese_game_company(C) & created_by(C, G)))).
fof(p3, axiom, ! [G] : (sold_over_one_million(G) => in_top_10(G))).
fof(p4, axiom, sold_over_one_million(legend_of_zelda)).
fof(goal, conjecture, ? [C] : (japanese_game_company(C) & created_by(C, fifa_22))).