% Axioms
fof(premise_jp_zelda, axiom, ? [C] : (japanese(C) & made_by(zelda, C))).
fof(premise_top10, axiom, ! [G] : (top10(G) => ? [C] : (japanese(C) & made_by(G, C))) ).
fof(premise_sales_top10, axiom, ! [G] : (sells_more_than_one_million(G) => top10(G))).
fof(premise_zelda_sales, axiom, sells_more_than_one_million(zelda)).
fof(distinct_zelda_fifa22, axiom, zelda != fifa22).
% Negated conjecture
fof(neg_conclusion, conjecture, ~ ? [C] : (japanese(C) & made_by(fifa22, C))).