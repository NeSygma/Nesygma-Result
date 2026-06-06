% Positive version: original claim as conjecture
% Premises:
% 1. A Japanese game company created the game the Legend of Zelda.
fof(premise_1, axiom, japanese_company_created(legend_of_zelda)).

% 2. All games on the Top 10 list are made by Japanese game companies.
fof(premise_2, axiom, ! [G] : (on_top_10_list(G) => made_by_japanese_company(G))).

% 3. If a game sells more than one million copies, then it will be included in the Top 10 list.
fof(premise_3, axiom, ! [G] : (sells_over_million(G) => on_top_10_list(G))).

% 4. The Legend of Zelda sold more than one million copies.
fof(premise_4, axiom, sells_over_million(legend_of_zelda)).

% Distinct entities
fof(distinct, axiom, (legend_of_zelda != fifa_22)).

% Conclusion: FIFA 22 is made by a Japanese video game company.
fof(goal, conjecture, made_by_japanese_company(fifa_22)).