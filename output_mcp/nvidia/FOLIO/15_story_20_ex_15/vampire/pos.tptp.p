% Axioms and conjecture for positive run
fof(axiom_1, axiom, created_by_japanese_company(zelda)).
fof(axiom_2, axiom, ! [X] : (top_ten(X) => made_by_japanese_company(X))).
fof(axiom_3, axiom, ! [X] : (sells_more_than_one_million(X) => top_ten(X))).
fof(axiom_4, axiom, sells_more_than_one_million(zelda)).
fof(conjecture_pos, conjecture, ~top_ten(zelda)).