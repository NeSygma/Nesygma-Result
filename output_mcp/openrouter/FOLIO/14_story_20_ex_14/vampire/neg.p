% Negative version
fof(jp_company_nintendo, axiom, japanese_company(nintendo)).
fof(created_zelda, axiom, created(nintendo, legend_of_zelda)).
fof(sells_zelda, axiom, sells_over_million(legend_of_zelda)).
fof(rule_top10_made_by_jp, axiom, ![G] : (top10(G) => ?[C] : (japanese_company(C) & created(C,G)))).
fof(rule_sells_top10, axiom, ![G] : (sells_over_million(G) => top10(G))).
fof(distinct_consts, axiom, (nintendo != fifa_22 & nintendo != legend_of_zelda & fifa_22 != legend_of_zelda)).
fof(goal, conjecture, ![C] : ~(japanese_company(C) & created(C, fifa_22))).