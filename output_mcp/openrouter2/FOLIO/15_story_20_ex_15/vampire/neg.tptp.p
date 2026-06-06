fof(japanese_company_company_a, axiom, japanese_company(company_a)).
fof(created_by_zelda_company_a, axiom, created_by(zelda, company_a)).
fof(sells_more_than_zelda, axiom, sells_more_than(zelda)).
fof(rule_sells_top10, axiom, ![G] : (sells_more_than(G) => top10(G))).
fof(rule_top10_japanese, axiom, ![G] : (top10(G) => ![C] : (created_by(G, C) => japanese_company(C)))).
fof(distinct_zelda_company_a, axiom, zelda != company_a).
fof(conjecture, conjecture, top10(zelda)).