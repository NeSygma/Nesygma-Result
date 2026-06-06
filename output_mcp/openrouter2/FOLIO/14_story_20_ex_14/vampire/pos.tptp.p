fof(jp_fact, axiom, japanese_company(j_company) & created(j_company, legend_of_zelda)).
fof(sells_fact, axiom, sells_more_than_one_million(legend_of_zelda)).
fof(sells_rule, axiom, ! [G] : (sells_more_than_one_million(G) => top10(G))).
fof(top10_rule, axiom, ! [G] : (top10(G) => ? [C] : (japanese_company(C) & created(C, G)))).
fof(conjecture, conjecture, ? [C] : (japanese_company(C) & created(C, fifa_22))).