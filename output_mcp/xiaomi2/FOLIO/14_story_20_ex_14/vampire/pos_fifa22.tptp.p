fof(p1, axiom, ? [X] : (japanese_company(X) & created(X, legend_of_zelda))).
fof(p2, axiom, ! [Y] : (on_top_10(Y) => ? [X] : (japanese_company(X) & created(X, Y)))).
fof(p3, axiom, ! [Y] : (sold_over_million(Y) => on_top_10(Y))).
fof(p4, axiom, sold_over_million(legend_of_zelda)).
fof(goal, conjecture, ? [X] : (japanese_company(X) & created(X, fifa_22))).