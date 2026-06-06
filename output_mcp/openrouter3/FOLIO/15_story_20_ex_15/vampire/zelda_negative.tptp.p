% Negative version: The Legend of Zelda IS on the Top 10 list (negation of conclusion)
fof(japanese_company_created_zelda, axiom, ? [C] : (japanese_company(C) & created(C, zelda))).
fof(top10_made_by_japanese, axiom, ! [G] : (on_top10(G) => ? [C] : (japanese_company(C) & created(C, G)))).
fof(sells_million_implies_top10, axiom, ! [G] : (sells_million(G) => on_top10(G))).
fof(zelda_sells_million, axiom, sells_million(zelda)).
fof(distinct_entities, axiom, (zelda != nintendo & zelda != sony & nintendo != sony)).
fof(goal, conjecture, on_top10(zelda)).