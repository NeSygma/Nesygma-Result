fof(premise_1, axiom, ? [C] : (japanese_company(C) & made_by(zelda, C))).
fof(premise_2, axiom, ! [G] : (top10(G) => ? [C] : (japanese_company(C) & made_by(G, C)))).
fof(premise_3, axiom, ! [G] : (sells_million(G) => top10(G))).
fof(premise_4, axiom, sells_million(zelda)).
fof(distinct_games, axiom, (zelda != fifa22)).
fof(goal, conjecture, ? [C] : (japanese_company(C) & made_by(fifa22, C))).