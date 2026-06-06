fof(axiom_sells_to_top10, axiom, ! [X] : (sells_more_than_one_million(X) => on_top_10(X))).
fof(fact_sells, axiom, sells_more_than_one_million(legend_of_zelda)).
fof(conjecture, conjecture, ~on_top_10(legend_of_zelda)).