fof(premise1, axiom, ?[C] : (japanese_company(C) & made_by(legend_of_zelda, C))).
fof(premise2, axiom, ![G] : (top10(G) => ?[C] : (japanese_company(C) & made_by(G, C)))).
fof(premise3, axiom, ![G] : (sells_more_than_one_million(G) => top10(G))).
fof(premise4, axiom, sells_more_than_one_million(legend_of_zelda)).
fof(conjecture, conjecture, top10(legend_of_zelda)).