fof(premise1, axiom, made_by_japanese(zelda)).
fof(premise2, axiom, ! [G] : (on_top10(G) => made_by_japanese(G))).
fof(premise3, axiom, ! [G] : (sells_more_than_one_million(G) => on_top10(G))).
fof(premise4, axiom, sells_more_than_one_million(zelda)).
fof(conclusion, conjecture, ~on_top10(zelda)).