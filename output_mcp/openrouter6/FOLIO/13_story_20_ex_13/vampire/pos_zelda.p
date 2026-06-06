fof(premise1, axiom, ? [C] : (japanese_company(C) & created(C, zelda))).
fof(premise2, axiom, ! [G] : (top10(G) => ? [C] : (japanese_company(C) & created(C, G)))).
fof(premise3, axiom, ! [G] : (sells_million(G) => top10(G))).
fof(premise4, axiom, sells_million(zelda)).
fof(conclusion, conjecture, top10(zelda)).