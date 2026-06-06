fof(p1, axiom, ? [C] : (japanese_company(C) & created(C, zelda))).
fof(p2, axiom, ! [G] : (on_top_10(G) => ? [C] : (japanese_company(C) & created(C, G)))).
fof(p3, axiom, ! [G] : (sold_over_million(G) => on_top_10(G))).
fof(p4, axiom, sold_over_million(zelda)).
fof(goal, conjecture, ~on_top_10(zelda)).