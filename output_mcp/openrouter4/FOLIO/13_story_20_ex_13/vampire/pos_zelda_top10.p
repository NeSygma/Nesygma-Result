% Positive version: original claim as conjecture
fof(premise_1, axiom, created_by_japanese_company(zelda)).
fof(premise_2, axiom, ! [X] : (on_top_10_list(X) => created_by_japanese_company(X))).
fof(premise_3, axiom, ! [X] : (sells_more_than_million(X) => on_top_10_list(X))).
fof(premise_4, axiom, sells_more_than_million(zelda)).
fof(goal, conjecture, on_top_10_list(zelda)).