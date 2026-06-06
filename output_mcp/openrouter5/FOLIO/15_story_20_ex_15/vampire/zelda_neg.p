% Negative version: negated conclusion as conjecture
% Original conclusion: ~on_top_10(legend_of_zelda)
% Negated conclusion: on_top_10(legend_of_zelda)

fof(premise_1, axiom, japanese_game_company(japanese_company)).
fof(created_game, axiom, created(japanese_company, legend_of_zelda)).

fof(premise_2, axiom, ! [G] : (on_top_10(G) => japanese_game_company(maker_of(G)))).

fof(premise_3, axiom, ! [G] : (sells_more_than_one_million(G) => on_top_10(G))).

fof(premise_4, axiom, sells_more_than_one_million(legend_of_zelda)).

fof(goal_neg, conjecture, on_top_10(legend_of_zelda)).