% Positive version: Legend of Zelda is on Top 10 list
fof(distinct_entities, axiom, (zelda != top10_list)).
fof(premise_1, axiom, ? [C] : (japanese_company(C) & created(C, zelda))).
fof(premise_2, axiom, ! [G] : (on_top10(G) => ? [C] : (japanese_company(C) & created(C, G)))).
fof(premise_3, axiom, ! [G] : (sells_million(G) => on_top10(G))).
fof(premise_4, axiom, sells_million(zelda)).
fof(goal, conjecture, on_top10(zelda)).