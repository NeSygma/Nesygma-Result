fof(japanese_company_created, axiom,
    ? [X] : (japanese_company(X) & created(X, legend_of_zelda))).

fof(top10_japanese, axiom,
    ! [Y] : (on_top_10(Y) => ? [X] : (japanese_company(X) & created(X, Y)))).

fof(sold_to_top10, axiom,
    ! [Y] : (sold_more_than_million(Y) => on_top_10(Y))).

fof(zelda_sold, axiom,
    sold_more_than_million(legend_of_zelda)).

fof(goal, conjecture,
    ~on_top_10(legend_of_zelda)).